import pymysql
import time
import json
import os

while (1):
    first_boot = 1
    try:
        connection_to_toko = 1

        try:
            connToko = pymysql.connect(host='localhost', user='root', passwd='', db='db_tokoims', port=3306)
            curToko = connToko.cursor()
        except:
            print("can't connect to TOKO")

        try:
            connBank = pymysql.connect(host='localhost', user='root', passwd='', db='db_bankims', port=3306)
            curBank = connBank.cursor()
        except:
            print("can't connect to BANK")


        sql_select = "SELECT * FROM tb_transaksi"
        curBank.execute(sql_select)
        result = curBank.fetchall()

        sql_select = "SELECT * FROM tb_integrasi"
        curBank.execute(sql_select)
        integrasi = curBank.fetchall()

        print("result len = %d | integrasi len = %d" % (len(result), len(integrasi)))

        # insert listener
        if (len(result) > len(integrasi)):
            print("-- INSERT DETECTED --")
            for data in result:
                a = 0
                for dataIntegrasi in integrasi:
                    if (data[0] == dataIntegrasi[0]):
                        a = 1
                if (a == 0):
                    print("-- RUN INSERT FOR ID = %s" % (data[0]))
                    val = (data[0], data[3])
                    insert_integrasi_bank = "insert into tb_integrasi (id_transaksi, status) values(%s,%s)"
                    curBank.execute(insert_integrasi_bank, val)
                    connBank.commit()

                    if (connection_to_toko == 1):
                        insert_integrasi_toko = "insert into tb_integrasi (id_transaksi, status) values(%s,%s)"
                        curToko.execute(insert_integrasi_toko, val)
                        connToko.commit()

                        insert_transaksi_toko = "insert into tb_transaksi (id_transaksi, status) values(%s,%s)"
                        curToko.execute(insert_transaksi_toko, val)
                        connToko.commit()



        # delete listener
        if (len(result) < len(integrasi)):
            print("-- DELETE DETECTED --")
            for dataIntegrasi in integrasi:
                a = 0
                for data in result:
                    if (dataIntegrasi[0] == data[0]):
                        a = 1
                if (a == 0):
                    print("-- RUN DELETE FOR ID = %s" % (dataIntegrasi[0]))
                    delete_integrasi_bank = "delete from tb_integrasi where id_transaksi = %s" % (dataIntegrasi[0])
                    curBank.execute(delete_integrasi_bank)
                    connBank.commit()

                    if (connection_to_toko == 1):
                        delete_integrasi_toko = "delete from tb_integrasi where id_transaksi = %s" % (dataIntegrasi[0])
                        curToko.execute(delete_integrasi_toko)
                        connToko.commit()

                        delete_transaksi_toko = "delete from tb_transaksi where id_transaksi = %s" % (dataIntegrasi[0])
                        curToko.execute(delete_transaksi_toko)
                        connToko.commit()


        # update listener
        if (result != integrasi):
            print("-- EVENT SUCCESS OR UPDATE DETECTED --")
            for data in result:
                for dataIntegrasi in integrasi:
                    if (data[0] == dataIntegrasi[0]):
                        if (data != dataIntegrasi):
                            val = (data[3], data[0])
                            update_integrasi_bank = "update tb_integrasi set status = %s where id_transaksi = %s"
                            curBank.execute(update_integrasi_bank, val)
                            connBank.commit()

                            if (connection_to_toko == 1):
                                update_integrasi_toko = "update tb_integrasi set status = %s where id_transaksi = %s"
                                curToko.execute(update_integrasi_toko, val)
                                connToko.commit()

                                update_transaksi_toko = "update tb_transaksi set status = %s where id_transaksi = %s"
                                curToko.execute(update_transaksi_toko, val)
                                connToko.commit()



    except (pymysql.Error, pymysql.Warning) as e:
        print(e)

    # Untuk delay
    time.sleep(4)
