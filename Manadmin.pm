package Manadmin;

use ManateeSQL;

sub dumpTable{
	my ($sql,$table,$file) = @_;
     if(&ManateeSQL::table_exists($sql,$table)){
		my $cmd = qq(SHOW CREATE TABLE $table;);
		$result = &ManateeSQL::doQuery(0,$sql,$cmd);
		if ($result) {
			print $file "$result->[1]";
		}
		my $cmd = qq(SELECT * FROM $table;);
		$result = &ManateeSQL::doQuery(1,$sql,$cmd);
		$cmd = qq(SHOW COLUMNS FROM $table);
		$columns = &ManateeSQL::doQuery(1,$sql,$cmd);
		foreach my $row (@{$result}) {
			my $line = "INSERT INTO $table (";
			my $line2 = ") VALUES(";
			foreach my $cname (@{$columns}) {
				$line = "$line$cname->{Field},";
				$line2 = "$line2'$row->{$cname->{Field}}',";
			}
			$line = substr($line,0,length($line)-1);
			$line2 = substr($line2,0,length($line2)-1);
			$line2 = "$line2);\n";
			print $file "$line$line2";
		}
		return 0;
	} else {
		return -1;
	}
}

1;