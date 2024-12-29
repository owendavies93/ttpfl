package TTPFL::Points;

use Mojo::Base 'Exporter';

our @EXPORT_OK = qw(get_weighted_points);

use Const::Fast;
use List::Util qw(sum);

const my @first_mondays => (
    '20240101',
    '20240205',
    '20240304',
    '20240401',
    '20240506',
    '20240603',
    '20240701',
    '20240805',
    '20240902',
    '20241007',
    '20241104',
    '20241202',
);

const my $debug => 0;

# Assumes we're looking back at 2024
sub get_weighted_points {
    my ($player_id, $weights, $ranking_data, $eoy_points) = @_;

    my $points = {};
    for my $row (@$ranking_data) {
        my ($date, $rank, $player, $ps) = @$row;
        if ($player == $player_id) {
            $points->{$date} = $ps;
        }
    }

    my @month_starts = reverse @first_mondays;
    my $last = $eoy_points->{$player_id};
    my $months = 1;
    my $total_points = 0;
    for my $month_start (@month_starts) {
        my ($current_month) = $month_start =~ /\d{4}(\d{2})\d{2}/;
        $current_month = int($current_month);

        if (exists $points->{$month_start}) {
            _debug("Points for $month_start: $points->{$month_start} ($months) ($last)");
            my $delta = $last - $points->{$month_start};
            my $per_month = $delta / $months;
            _debug("Delta: $delta");

            my $start_month = $current_month + $months;
            _debug("Start month: $start_month");

            for my $i (1 .. $months) {
                my $tmp_month = $start_month - $i;
                _debug("Weight for $tmp_month: $weights->{$tmp_month}");
                $total_points += $per_month * $weights->{$tmp_month};
            }

            $last = $points->{$month_start};
            $months = 1;
        } else {
            _debug("No points for $month_start");
            $months++;
        }
    }

    my $weight_sum = sum values %$weights;
    $total_points = int($total_points / $weight_sum);
    _debug("Total points: $total_points");
    return $total_points;
}

sub _debug {
    say @_ if $debug;
}

1;
