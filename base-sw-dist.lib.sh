#This is a script library that can be sourced by bash scripts to define ENV variables and functions.
#



function local_environment {

export LOCAL_SW_ROOT=${LOCAL_SW_ROOT:-/opt/local}


case "$1" in
  set)
    export LOCAL_SW_ETC
    export LOCAL_SW_VAR
    export LOCAL_SW_SCRIPT_LIBS
    export PATH=$PATH:$LOCAL_SW_ROOT/bin:$LOCAL_SW_ROOT/sbin
    export MANPATH=:$LOCAL_SW_ROOT/share/man
    export LOCAL_HOSTNAME=$(hostname -s)
    export LOCAL_FQDN=$(hostname -f)
    ;;
  unset)
    # Strip out PATH addition for /bin
    export PATH=${PATH//$LOCAL_SW_ROOT\/bin/}
    
    # Strip out PATH addition for /sbin
    export PATH=${PATH//$LOCAL_SW_ROOT\/sbin/}
    
    # Remove trailing : twice for each path
    export PATH=${PATH%:}
    export PATH=${PATH%:}
    # Remove leading :
    export PATH=${PATH#:}
    export PATH=${PATH#:}
    
    unset MANPATH
    ;;
  get)
    ;;
  path_override)
    export PATH=$LOCAL_SW_ROOT/bin:$LOCAL_SW_ROOT/sbin:$PATH
    export MANPATH=$LOCAL_SW_ROOT/share/man:
    ;;
  *)
    ;;

esac

}

