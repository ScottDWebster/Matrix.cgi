#!/usr/bin/perl
#!/usr/local/bin/perl
#!/perl/5.00502/bin/MSWin32-x86-object/perl.exe

$|=1;

if(defined $ENV{'SERVER_NAME'})
{
	print "Content-type: text/html\n\n";
	print "<html><head>\n";
	print "<title>Invert a random matrix using the Gauss-Jordan method</title>\n";
	print "</head><body><pre>\n";
}
if(IsWin95 | IsWinNT)
{
	srand();
}else
{
	srand(time()^($$+($$<<15)));
}

if(defined $ENV{'QUERY_STRING'} & $ENV{'QUERY_STRING'} =~ /^\s*\d+\s*$/) 
{
		$size = $ENV{'QUERY_STRING'};
}elsif(defined $ARGV[0] & $ARGV[0] =~ /^\s*\d+\s*$/)
{
		$size = $ARGV[0];
}
unless(defined $size)
{
	$size = int(rand 7) + 3;
}
if($size < 3)
{
	$size = 3;
}elsif($size > 9)
{
	$size = 9;
}
$dblsize = $size * 2;

for($i = 0; $i < $size; $i++)
{
	for($j = 0; $j < $size; $j++)
	{
		$matrix[$i][$j] = int(rand 10);
	}
}

## Save a copy of original matrix
for($i = 0; $i < $size; $i++)
{
	for($j = 0; $j < $size; $j++)
	{
		$origmat[$i][$j] = $matrix[$i][$j];
	}
}

## Create identity matrix
for($i = 0; $i < $size; $i++)
{
	for($j = 0; $j < $size; $j++)
	{
		if($i == $j)
		{
			$id[$i][$j] = 1;	
		}else
		{
			$id[$i][$j] = 0;
		}
	}
}

## Append identity matrix
for($i = 0; $i < $size; $i++)
{
	push @{${matrix[$i]}}, @{${id[$i]}}; 
}
print "Starting matrix:\n\n";
&printmatrix;

## Invert matrix
for($i = 0; $i < $size; $i++)
{
	if(&make1)
	{
		&printmatrix;
	}
	&make0;
}

print " ", "-" x ((8 * $dblsize) + 3), "\n\n";

$omtxt = "Original Matrix";
$imtxt = "Inverted Matrix";
print " $omtxt",  " " x ((8 * $size) - length($omtxt) + 5), "$imtxt\n\n";

for($i = 0; $i < $size; $i++)
{
	for($j = 0; $j < $dblsize; $j++)
	{
		printf("%7.3f ", $origmat[$i][$j]) if($j<$size);
		print " " x 5 if($j==$size);
		printf("%7.3f ", $matrix[$i][$j]) if($j>=$size);
	}
	print "\n";
}
print "\n";

if(defined $ENV{'SERVER_NAME'})
{
	print "</pre></body></html>\n";
}

###################
### Subroutines ###
###################

## Print out matrix
sub printmatrix
{
	my($i, $j);
	for($i = 0; $i < $size; $i++)
	{
		for($j = 0; $j < $dblsize; $j++)
		{
			printf("%7.3f ", $matrix[$i][$j]);
		}
		print "\n";
	}
	print "\n";
}

sub make1
{
	my ($i1, $is1, $didstuff, $divnum, $j, $k, $l, $m, $n);
	$didstuff = 0;
	$i1 = $i + 1;
	unless($matrix[$i][$i] == 1)
	{
		unless($matrix[$i][$i] == 0)
		{
			$divnum = $matrix[$i][$i];
			for($j = 0;$j < $dblsize; $j++)
			{
				$matrix[$i][$j] /= $divnum;
			}
			$didstuff = 1;
			print "Row $i1 = Row $i1 / $divnum:\n\n";
		}else
		{
			undef $is1;
			for($k = 0; $k < $size; $k++)
			{
				unless($k == $i)
				{
					$is1 = $k if($matrix[$k][$i] == 1);
				}
			}
			if(defined $is1)
			{
				for($l = 0; $l < $dblsize; $l++)
				{
					$matrix[$i][$l] += $matrix[$is1][$l];
				}
				$didstuff = 1;
				print "Row $i1 = Row $i1 + Row ", $is1+1, ":\n\n";
			}else
			{
				for($m = $#matrix; $m > 0; $m--)
				{
					unless($m == $i)
					{
						if($matrix[$m][$i])
						{
							$divnum = $matrix[$m][$i];
							for($n = 0; $n < $dblsize; $n++)
							{
								$matrix[$i][$n] += $matrix[$m][$n] / $divnum;
							}
							$didstuff = 1;
							print "Row $i1 = Row $i1 + Row $m / $divnum:\n\n";
							$m = -1;
						}
					}
				}
			}
		}
	}	
	return $didstuff;
}

sub make0
{
	my ($timesnum, $i1, $k, $j);
	$i1 = $i + 1;
	for($j = 0; $j < $size; $j++)
	{
		$j1 = $j + 1;
		unless($j == $i)
		{
			if($matrix[$j][$i])
			{
				$timesnum = $matrix[$j][$i];
				for($k = 0; $k < $dblsize; $k++)
				{
					$matrix[$j][$k] -= $matrix[$i][$k] * $timesnum
				}
				print "Row $j1 = Row $j1 - Row $i1 * $timesnum:\n\n";
				&printmatrix;
			}
		}
	}
}
