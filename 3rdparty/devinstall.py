#Copyright 2013 Avi Networks
#!python
import apt
import sys
import apt_pkg
import os.path
import subprocess

def checkninstall_pythonapt():
    cache = apt.Cache()
    pkg = cache['python-apt'] # Access the Package object for python-apt
    print 'python-apt is trusted:', pkg.candidate.origins[0].trusted
    # Mark python-apt for install
    pkg.mark_install()
    print 'python-apt is marked for install:', pkg.marked_install
    print 'python-apt is (summary):', pkg.candidate.summary
    # Now, really install it
    cache.commit()

def apt_get_wrapper(pkgname):
    subprocess.call(['apt-get','install',pkgname],stderr=subprocess.STDOUT)
    
def check_n_install_pkg(pkgname, pkg_data):
    cache = apt.Cache()
    pkg = cache[pkgname]
    
    if (pkg is not None) and (pkg.is_installed is True):
        print pkgname, ' is installed', pkg.installed
        return

    print pkgname, ' is not installed. Adding to install'
    if ('version' in pkg_data):
        # this is case when version number is specified
        pkg_ver = pkg_data['version']
        print 'installing ',pkgname, ' with version ',pkg_ver
        apt_get_wrapper(str(pkgname+'='+pkg_ver))
    else:
        pkg.mark_install()
        cache.commit()



        
def install_gtest():
    gtest_path = '/usr/local/lib/libgtest.so'
    if (os.path.exists(gtest_path) is not True) or (os.access(gtest_path, os.X_OK) is not True) :
        # call the gtest_install.s
        print 'Google Test is not installed. Installing'
        subprocess.check_output(["./gtest_install.sh"],stderr=subprocess.STDOUT)
        
    else:
        print 'Google Test already installed'
    


def install_redis():
    redis_path = '/usr/bin/redis-server'
    if (os.path.exists(redis_path) is not True) or (os.access(redis_path, os.X_OK) is not True) :
        print 'redis server is not installed. Installing...'
        subprocess.check_output(["./redis_install.sh"],stderr=subprocess.STDOUT)
        print 'redis server is now installed'
    else:
        print 'redis server is already installed'
        
def install_linux_source_pkgs():    
    install_gtest()
    install_redis()

def install_linux_pkgs(pkg_list):
    
    for pkg,pkg_data in pkg_list.iteritems():
        check_n_install_pkg(pkg,pkg_data)

def init_linux_pkgs():
    # if a particular version needs to be installed then you can add
    # an entry 'version':<version> for any of the
    # module. libboost-system-dev is just and example here.
    # 'libboost-system-dev' : {'version':'1.49.0.1'},
    linux_pkgs = {
        'libboost-system-dev' : {},
        'libboost-dev' : {},
#        'libgoogle-glog-dev' : {},
        'libgtest-dev' : {},
        'protobuf-compiler' : {},
        'libboost-thread-dev' : {},
        'libprotobuf-dev' : {},
        'libboost-python-dev' :{},
        'libhiredis-dev':{},
	'eclipse':{},
	'emacs':{},
        'ia32-libs':{},
        'curl':{},
        #'doxygen':{},
        }

    return linux_pkgs

def main(_args):
    checkninstall_pythonapt()
    print "Checking and Installing AVI dependent packages"
    
    pkgs_list = init_linux_pkgs()    
    install_linux_pkgs(pkgs_list)
    install_linux_source_pkgs()


if __name__ == '__main__':
    sys.exit(main(sys.argv))

