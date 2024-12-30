package TTPFL::Players;

use Mojo::Base 'Exporter';

our @EXPORT_OK = qw(get_player_from_last_name_initial);

sub get_player_from_last_name_initial {
    my ($last_name, $initial, $players) = @_;

    $initial =~ s/\.//;

    my @candidates;
    for my $player (@$players) {
        my ($fn, $ln) = split /\s+/, $player;
        if ($ln eq $last_name && substr($fn, 0, 1) eq $initial) {
            push @candidates, $player;
        }
    }

    if (scalar @candidates == 1) {
        return $candidates[0];
    } elsif (scalar @candidates > 1) {
        die "Multiple candidates for $last_name $initial: @candidates";
    }

    return undef;
}

1;
