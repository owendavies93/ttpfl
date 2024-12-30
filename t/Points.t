use Mojo::Base -strict;

use lib 'lib';

use Test::More;
use TTPFL::Points qw(get_baseline_points get_weighted_deltas);

# Test get_baseline_points
subtest 'get_baseline_points' => sub {
    my $gs_points = {
        1 => 2000,
        2 => 1300,
        4 => 800,
        8 => 400,
        16 => 200,
        32 => 100,
        64 => 50,
        128 => 10,
    };

    is(get_baseline_points(123, $gs_points, 1), 2000, 'Rank 1 gets points for top 1');
    is(get_baseline_points(123, $gs_points, 5), 400, 'Rank 5 gets points for top 8');
    is(get_baseline_points(123, $gs_points, 15), 200, 'Rank 15 gets points for top 16');
    is(get_baseline_points(123, $gs_points, 30), 100, 'Rank 30 gets points for top 32');
    is(get_baseline_points(123, $gs_points, 75), 10, 'Rank 75 gets points for top 128');
    is(get_baseline_points(123, $gs_points, 150), 0, 'Rank 150 gets no points');
};

# Test get_weighted_deltas
subtest 'get_weighted_deltas' => sub {
    my $weights = {
        1 => 12,
        2 => 10,
        3 => 8,
        4 => 6,
        5 => 4,
        6 => 2,
        7 => 1,
        8 => 0,
        9 => 0,
        10 => 0,
        11 => 0,
        12 => 0,
    };

    my $ranking_data = [
        ['20240101', 10, 999, 1000],  # January
        ['20240304', 15, 999, 800],   # March
        ['20240506', 20, 999, 500],   # May
    ];

    my $eoy_points = {
        999 => [undef, 1200]  # End of year points
    };

    my $result = get_weighted_deltas(999, $weights, $ranking_data, $eoy_points);
    ok(defined $result, 'Returns a defined value');
    is(ref $result, '', 'Returns a scalar');
    like($result, qr/^-?\d+$/, 'Returns an integer');
    is($result, -85, 'Returns the correct value');
};

done_testing();
