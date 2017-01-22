#!bin/bash
SETCOLOR_SUCCESS="echo -n \\033[1;32m"
SETCOLOR_FAILURE="echo -n \\033[1;31m"
SETCOLOR_NORMAL="echo -n \\033[0;39m"

echo "Будут выполнены следующие скрипты:"
for file in $1*.sql
do
    echo $file
done

echo -n "Нажмите Enter для подтверждения... "
read nothing

for file in $1*.sql
do
    mysql -t -u freebee -p221uml?Po < $file
    if [ $? -eq 0 ]; then
        $SETCOLOR_SUCCESS
        echo $file "[OK]"
        $SETCOLOR_NORMAL
    else
        $SETCOLOR_FAILURE
        echo $file "[fail]"
        $SETCOLOR_NORMAL
    fi
done
