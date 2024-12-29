package TTPFL::Config;

use Mojo::Base 'Exporter';

use YAML::XS;

our @EXPORT_OK = qw(get_weights);

sub get_weights {
    my $file = 'etc/weights.yaml';
    my $config = YAML::XS::LoadFile($file);
    return $config->{weights};
}

1;
