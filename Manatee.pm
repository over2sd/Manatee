package Manatee;

use Cwd;

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
		'custom' => chooseStyle($style)
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