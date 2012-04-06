#!/bin/sh

NAME="blacklist"
USER="_nginx"
GROUP="_nginx"
SOCKETDIR="/www/blacklist/fcgi"
PIDDIR="/var/run/blacklist"

function prepare {
	test -d ${SOCKETDIR} || mkdir -p ${SOCKETDIR}
	test -d ${PIDDIR} || mkdir -p ${PIDDIR}
	chown -R _nginx:_nginx ${SOCKETDIR} ${PIDDIR}
}

function cleanup {
	test -f ${SOCKETDIR}/${NAME}.${1}.sock && \
		rm -f ${SOCKETDIR}/${NAME}.${1}.sock
	test -f ${PIDDIR}/${NAME}.${1}.pid && \
		rm -f ${PIDDIR}/${NAME}.${1}.pid
}

function fcgi_start {
	cd /www/blacklist/app
	sudo -u ${USER} /usr/local/bin/python manage.py runfcgi \
		method=threaded \
		socket=${SOCKETDIR}/${NAME}.${1}.sock \
		daemonize=true \
		maxchildren=1 \
		pidfile=${PIDDIR}/${NAME}.${1}.pid
	chown ${USER}:${GROUP} ${SOCKETDIR}/${NAME}.${1}.sock
	chmod o-rwx ${SOCKETDIR}/${NAME}.${1}.sock
}

function fcgi_stop {
	test -f ${PIDDIR}/${NAME}.${1}.pid && \
		kill `cat ${PIDDIR}/${NAME}.${1}.pid` 2>/dev/null
	rm -f ${PIDDIR}/${NAME}.${1}.pid
}

case "${1}" in
	start)
		echo -n ' blacklist('
		prepare
		for i in 0 1 2 3 4; do
			echo -n "${i}"
			fcgi_start ${i}
		done
		echo ').'
		;;
	stop)
		echo -n ' blacklist('
		for i in 0 1 2 3 4; do
			echo -n "${i}"
			fcgi_stop ${i}
		done
		cleanup
		echo ').'
		;;
	restart)
		${0} stop
		sleep 1
		${0} start
		;;
	*)
		echo "Usage: `basename ${0}` <start|stop|restart>"
		exit 1
		;;
esac

exit 0
