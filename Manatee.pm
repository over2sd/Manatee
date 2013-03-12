package Manatee;

require Exporter;
@ISA = qw(Exporter);
@EXPORT = qw(chooseStyle getStage);

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

sub getStage{
	my ($code) = @_;
	my $loc = index($code,'x');
	if($loc gt 0){ $loc = 4; }
	if($code == "XXXX"){ $loc = 0; }
	return $loc;
}



1;