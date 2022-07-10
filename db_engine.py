import os
import sqlite3

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


# Using this class rsa encryption has been done using private key form file "key.pem"
class RsaEncryption():
    _file = "key.pem"

    @classmethod
    def _load(cls):
        with open(cls._file, 'rb') as data_file:
            data_lines = data_file.read()
            cls._private_key = load_pem_private_key(data_lines, None)
            cls._public_key = cls._private_key.public_key()
        print("key loaded successfully from 'key.pem' ")

    @classmethod
    def _save(cls):
        key_data = cls._private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption())
        with open(cls._file, 'wb') as data_file:
            data_file.write(key_data)
        print("key saved successfully")

    @classmethod
    def init(cls):
        if os.path.exists(cls._file):
            cls._load()

        else:
            cls._private_key = rsa.generate_private_key(public_exponent=65537,
                                                        key_size=2048)
            cls._public_key = cls._private_key.public_key()
            cls._save()

    @classmethod
    def encrypt(cls, data):
        def _encrypt(data_str):
            if type(data_str) is str:
                return cls._public_key.encrypt(bytes(data_str, 'utf-8'),
                                               padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                            algorithm=hashes.SHA256(), label=None))
            else:
                return data_str

        if type(data) is dict:
            for key in data.keys():
                data[key] = _encrypt(data[key])
            return data
        elif type(data) is list:
            for item in data:
                for key in item.keys():
                    item[key] = _encrypt(item[key])
            return data
        else:
            return _encrypt(data)

    @classmethod
    def decrypt(cls, data):
        def _decrypt(bytes_data):
            if type(bytes_data) is bytes:
                return cls._private_key.decrypt(bytes_data, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                                         algorithm=hashes.SHA256(),
                                                                         label=None)).decode()
            else:
                return bytes_data

        if type(data) is dict:
            for key, val in data.items():
                data[key] = _decrypt(val)

        elif type(data) is list:
            for item in data:
                for key in item.keys():
                    item[key] = _decrypt(item[key])

        else:
            data = _decrypt(data)

        return data

# making database accessible for this project
class DataBase():
    def __init__(self, filepath):
        self._file = filepath

    def _decrypt(cls, bytes_data):
        if type(bytes_data) is bytes:
            return cls._private_key.decrypt(bytes_data, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                                     algorithm=hashes.SHA256(),
                                                                     label=None)).decode()
        else:
            return bytes_data

    def _connection(self):
        if not os.path.exists(self._file):
            print(f"file [{self._file}] not found ")

        else:
            try:
                return sqlite3.connect(self._file)
            except Exception as e:
                print(e)

    def selection(self, query, single):
        conn = self._connection()
        if conn is None:
            print("db connection not available")
        else:
            try:
                cursor = conn.cursor()
                cursor.execute(query)
                cols = [entry[0] for entry in cursor.description]
                data = cursor.fetchall()
                data = [{col: val for col, val in zip(cols, row)} for row in data]
                data = data[0] if single else data
                data = RsaEncryption.decrypt(data)
            except Exception as e:
                print(e);
                data = None
            finally:
                cursor.close()
                conn.close()
                return data

    def read(self, table):
        """ read settings from database table """
        connection = self._connection()
        if connection is None:
            print("can't read data - no connection is available")
            return None

        cursor = connection.cursor()
        data = None
        try:

            query = f'SELECT * FROM {table}'
            cursor.execute(query)

            # fetch all records
            data = cursor.fetchall()[0]
            # read column names from cursor
            cols = [item[0] for item in cursor.description]
            # convert data to dictionary
            data = {key: val for key, val in zip(cols, data)}
            # decrypt data
            data = self._decrypt(data)
            return data

        except Exception as e:
            print(f'[EXCEPTION] {e}')

        finally:
            cursor.close()
            connection.close()
            return data

    def save(self, table, row):
        conn = self._connection()
        if conn is None:
            print("db connection not available");
            return False
        else:
            try:
                result = False
                cols = ", ".join([col for col in row.keys()])
                row = RsaEncryption.encrypt(row)
                query = "INSERT INTO {}({}) VALUES({})".format(table, cols,
                                                               ", ".join(["?"] * len(row.values())))
                cursor = conn.cursor()
                cursor.execute(query, tuple(row.values()))

            except Exception as error:
                print(error)
                try:
                    conn.rollback()
                except Exception:
                    pass

            else:
                conn.commit()
                result = True

            finally:
                cursor.close()
                conn.close()
                return result

    def update(self, tablename, new_data, where=""):
        conn = self._connection()
        if conn is None:
            print("db connection not available");
            return False
        else:
            try:
                result = False
                values_to_set = ", ".join([f"{col}=?" for col, val in new_data.items()])
                where = " WHERE " + where if where != "" else where
                query = "UPDATE {} SET {} {}".format(tablename, values_to_set, where)
                new_data = RsaEncryption.encrypt(new_data)
                cursor = conn.cursor()
                cursor.execute(query, tuple(new_data.values()))
            except Exception as e:
                print(e)
                try:
                    conn.rollback()
                except Exception:
                    pass

            else:
                conn.commit()
                result = True

            finally:
                cursor.close()
                conn.close()
                return result
