package TTPFL::Config;

use Mojo::Base 'Exporter';

use Const::Fast;
use YAML::XS;

our @EXPORT_OK = qw(get_weights get_gs_points);

const my $CONFIG_FILE => 'etc/config.yaml';

sub get_weights {
    my $config = _get_config();
    return $config->{weights};
}

sub get_gs_points {
    my $config = _get_config();
    return $config->{gs_points};
}

sub _get_config {
    my $config = YAML::XS::LoadFile($CONFIG_FILE);
    return $config;
}

1;
