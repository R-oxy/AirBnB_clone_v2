# Puppet manifest to set up web servers for web_static deployment

# Install Nginx (if not already installed)
package { 'nginx':
  ensure => 'installed',
}

# Create necessary directories
file { '/data/':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
  recurse => true,
}

file { '/data/web_static/':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

file { '/data/web_static/releases/':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

file { '/data/web_static/shared/':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

file { '/data/web_static/releases/test/':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

# Create a test HTML file
file { '/data/web_static/releases/test/index.html':
  ensure  => 'file',
  owner   => 'ubuntu',
  group   => 'ubuntu',
  content => '<html>\n  <head>\n  </head>\n  <body>\n    Holberton School\n  </body>\n</html>',
}

# Ensure the symbolic link is created (deleting and recreating if needed)
file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test',
  force  => true,
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

# Manage Nginx configuration
file { '/etc/nginx/sites-available/default':
  ensure  => 'file',
  owner   => 'root',
  group   => 'root',
  content => "
  server {
      listen 80;
      server_name 54.144.20.75;

      location /hbnb_static/ {
          alias /data/web_static/current/;
      }
  }
  server {
      listen 80;
      server_name 100.26.151.157;

      location /hbnb_static/ {
          alias /data/web_static/current/;
      }
  }
  ",
  notify  => Service['nginx'],
}

# Ensure Nginx service is running and enabled
service { 'nginx':
  ensure  => 'running',
  enable  => true,
}
