#!/usr/bin/perl -w

#get passed arguments
my $website = $ARGV[0];
my $password = $ARGV[1];

#output format

my @web = split(",", $website);
my @pass = split(",", $password);

for (@web) {
    $_ = $_ . "<br>"
}
for (@pass) {
    $_ = $_ . "<br>"
}

my $html = <<END;
<!DOCTYPE html>
<html>
    <body>
        <h2>Logged Websites and Passwords</h2>
        <table>
            <tr>
		<td>@web<td>
		<td>@pass<td>
            </tr>
        </table>
    <h2>Press Q to Return</h2>
    </body>
</html>
END

open(FH, ">", "./program_data/web_and_pass.html") or die $!;

print FH $html;

close(FH);

system("open", "./program_data/web_and_pass.html");
