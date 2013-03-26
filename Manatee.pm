package Manatee;

use Cwd;

sub suggVars{
	my ($lang,$build,$scod,$sdesc,$srat) = @_;
	my %var = (
		'title' => 'Default',
		'lang' => $lang,
		'build' => $build
	);

	return %var;
}

sub helpVars{
	my ($lang,$cowc,$dbh) = @_;
	my %var = (
		'title' => 'Default',
		'lang' => $lang
	);
	if (length($lang) == 0){
		$var{title} = "Select Language";
	} else {
		my $code = &Manatee::cleanCode($cowc);
		$var{title} = $code;
		$var{code} = $code;
		$var{y} = (substr($var{code},0,1) eq 'y') ? 1 : 0;
		$var{dosnip} = 1;
		$var{showsubs} = 0;
		$var{stage} = getStage($code);
		$var{catmul} = substr($code,0,$var{stage});
		$var{cattrim} = '';
		$var{catinf} = "cats/$lang/$code";
		if($var{stage} > 0){
			$var{cattrim} = $var{catmul};
		}
		if($var{stage} lt 4){
			$var{showsubs} = 1;
			while(length($var{catmul}) lt 4){
				$var{catmul} = "${var{catmul}}0";
			}
			$var{muldesc} = &ManateeSQL::glot($var{catmul},$dbh,$lang,4);
		}
		$var{catname} = &ManateeSQL::glot($var{code},$dbh,$lang,$var{stage});
		$var{border} = substr($var{catmul},0,3);
		if ($var{y}) { # explanation key
			$var{dosnip} = 0;
			$var{border} = "00" . substr($var{code},3,1);
			$var{title} = "Explanation of categories";
			if(substr($var{code},3,1) eq 'x' ) { # explain subcats
				$var{expl} = 1;
				$var{stage} = 3;
			} else { # explain a single subcat
				delete $var{catmul};
				$var{cattrim} = "*" . substr($var{code},3,1);
				$var{stage} = 4;
				delete $var{dosnip};
				$var{showsubs} = 0;
			}
		}
		$var{progress} = "View Progress Report";
	}
	return %var;
}

sub formClean{
	my ($s) = @_;
	$s =~ s/"/'/g;
	$s =~ s/\n/ /g;
	return $s;
}

sub loadConfig{
	my ($style) = @_;
	# TODO: sort out reading config file with Mason's paths and put it here
	my %config = (
		'site' => 'Manatee',
		'logo' => 'manateelogo.png',
		'logodesc' => 'Logo: drawing of a sea cow.',
		'custom' => chooseStyle($style),
		'localpath' => '/var/www/ccow-m'
	);
	return %config;
}

sub chooseStyle {
	my ($style) = @_;
	$style = substr($style,0,3);
	my %styledict = (
		'alt' => 'alpha'
	);
	my $out = '';
	if (length($styledict{$style})){
		$out = $styledict{$style};
	}
	return $out;
}

sub cleanCode {
	my ($code) = @_;
	while (length($code) < 4) {
		$code = $code . 'x';
	}
	$code = substr($code,0,4);
	for (my $i = 0; $i < length($code) and $i < 5; $i++) {
		$x = substr($code,$i,1);
		if (not "1234567890abcdefxyABCDEFX" =~ m/$x/) {
			substr($code,$i,1,'x');
		}
	}
	return $code;
}

sub getStage{
	my ($code) = @_;
	my $loc = index($code,'x');
	if($loc lt 0){ $loc = 4; }
	if($code eq "XXXX"){ $loc = 0; }
	if  (index($code,'y') == 1) { $loc = 3; }
	return $loc;
}

sub unSQL {
	my ($out) = @_;
	$out =~ s/~9/&/g;
	$out =~ s/~8/*/g;
	$out =~ s/~7/#/g;
	$out =~ s/~6/x/g;
	$out =~ s/~5/--/g;
	$out =~ s/~4/=/g;
	$out =~ s/~3/\"/g;
	$out =~ s/~2/\;/g;
	$out =~ s/~1/\'/g;
	$out =~ s/~0/~/g;
	return $out;
}

sub unhex {
	my ($hex) = @_;
	return hex($hex);
}

1;