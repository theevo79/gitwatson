import os


os.environ['DJANGO_DEBUG'] = 'False'
os.environ['DJANGO_SECRET_KEY'] = 'k5hy&b_&k3fs6(m$jv^cw*+&^hl(5iezmk$_(0k3+7$%_c2yvz'
os.environ['IBM_API_KEY'] = 'pJ-AKe9eWBAv1eTE4nIexYxLgeFBeAVGj7ETGkDNGhPG'

# current environment variables
if 'DJANGO_DEBUG' in os.environ:
    print('HOME environment variable is already defined. Value =', os.environ['IBM_API_KEY'])
else:
    print('HOME environment variable is not defined.')