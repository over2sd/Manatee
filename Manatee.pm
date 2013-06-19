package Manatee;

use Cwd;
use ManateeSQL;

sub suggVars{
	my ($lang,$cowc,$sdesc,$srat,$dbh) = @_;
	my %var = (
		'title' => 'Default',
		'lang' => $lang,
		'uri' => 'suggest.htm',
		'catinf' => 'bogus',
		'showform' => 1
	);
	if (length($lang) == 0){
		$var{title} = "Select Language";
	} else {
		my $code = cleanCode($cowc);
		$var{debug} = $code;
		$var{title} = "Suggest a Category";
		if (length($code) != 0){
			$var{cowc} = lc $code;
		} else {
			$var{showerr} = 1;
#			$var{cowc} = lc $code;
			$var{cowc} = "----";
			$var{error} = "Please provide a code to make a suggestion.";
		}
		$var{sdesc} = formClean($sdesc);
		$var{srat} = formClean($srat);
		$var{custom} = $var{style};
		if (substr($var{sdesc},0,1) == '[') {
			$var{showform} = 1;
		}
		if (($var{cowc} eq "xxxx") or ($var{cowc} =~ m/y/)) {
			$var{showerr} = 1;
			$var{showsubs} = 1;
			$var{error} = "Please choose a category to begin. You may not make suggestions for top-level or existing categories.";
		}
		if (!$var{showerr}) {
			$var{stage} = getStage($var{cowc});
			$var{catname} = &ManateeSQL::glot($var{cowc},$dbh,$lang,$var{stage});
			my $parent = substr("$var{cowc}xxxx",0,4);
			substr($parent,$var{stage}-1,1) = 'x';
			$var{parname} = &ManateeSQL::glot($parent,$dbh,$lang,$var{stage}-1);
			$var{catinf} = "cats/$lang/$parent";
			if (substr($var{parname},0,1) eq "[") {
				$var{showerr} = 1;
				$var{showform} = 0;
				$var{error} = "You cannot suggest a subcategory to an undefined category. Please choose another category.";
			} elsif (substr($var{catname},0,1) eq "[") {
				if (length($var{sdesc}) != 0 && substr($var{sdesc},0,1) ne "[" && length($var{srat}) > 19 && substr ($var{srat},0,1) ne "[") {
					$var{showform} = 0;
					$var{pushsugg} = 1; # if it's all good, insert a row into the suggestions table
				} else { # if bad input, display form
					$var{showform} = 1;
				}
			} else {
				$var{showerr} = 1;
				$var{showform} = 0;
				$var{showsubs} = 1;
				$var{cowc} = lc $code;
#				$var{cowc} = "----";
				$var{error} = "You have chosen an existing category. Please choose another category, or suggest a subcategory, if possible.";
			}
		}
	}
	return %var;
}

sub helpVars{
	my ($lang,$cowc,$dbh) = @_;
	my %var = (
		'title' => 'Default',
		'lang' => $lang,
		'uri' => 'index.htm',
		'catinf' => 'bogus'
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
		if (substr($var{catname},0,1) eq '[') {
			$var{suggsubs} = 1;
		}
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
		'localpath' => '/var/www/ccow-m',
		'sugurl' => 'suggest.htm'
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