package Manadmin;

use ManateeSQL;

sub dumpBase{
	my ($sql,$table,$file) = @_;
     if(&ManateeSQL::table_exists($sql,$table)){
		print "CREATE TABLE $table ( ccode CHAR(4) NOT NULL PRIMARY KEY, ctext VARCHAR(65) );\n";
		my $cmd = qq(SELECT * FROM $table LIMIT 100;);
#		print "?? $cmd ";
		$result = &ManateeSQL::doQuery(1,$sql,$cmd);
		foreach my $row (@{$result}) {
			print "INSERT INTO $table (ccode,ctext) VALUES('$row->{ccode}','$row->{ctext}');\n";
		}
		return 0;
	} else {
		return -1;
	}
}

1;