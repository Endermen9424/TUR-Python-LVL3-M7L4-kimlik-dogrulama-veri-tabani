import pytest
import sqlite3
import os
from registration.registration import create_db, add_user, authenticate_user, display_users

@pytest.fixture(scope="module")
def setup_database():
    """Testlerden önce veri tabanını oluşturmak ve testlerden sonra temizlemek için kullanılan test düzeneği."""
    create_db()
    yield
    try:
        os.remove('users.db')
    except PermissionError:
        pass

@pytest.fixture
def connection():
    """Test sırasında veri tabanı bağlantısı oluşturur ve testten sonra bağlantıyı kapatır."""
    conn = sqlite3.connect('users.db')
    yield conn
    conn.close()


def test_create_db(setup_database, connection):
    """Veri tabanı ve 'users' tablosunun oluşturulmasını test eder."""
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    table_exists = cursor.fetchone()
    assert table_exists, "'users' tablosu veri tabanında bulunmalıdır."

def test_add_new_user(setup_database, connection):
    """Yeni bir kullanıcının eklenmesini test eder."""
    add_user('testuser', 'testuser@example.com', 'password123')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username='testuser';")
    user = cursor.fetchone()
    assert user, "Kullanıcı veri tabanına eklenmiş olmalıdır."

# İşte yazabileceğiniz bazı testler:
"""
Var olan bir kullanıcı adıyla kullanıcı eklemeye çalışmayı test etme.
Başarılı kullanıcı doğrulamasını test etme.
Var olmayan bir kullanıcıyla doğrulama yapmayı test etme.
Yanlış şifreyle doğrulama yapmayı test etme.
Kullanıcı listesinin doğru şekilde görüntülenmesini test etme.
"""

def test_add_existing_user(setup_database, connection):
    """Var olan bir kullanıcı adıyla kullanıcı eklemeye çalışmayı test eder."""
    add_user("Ali", "ali@example.com", "123456")
    add_user("Ali", "ali@example.com", "123456")

    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM users WHERE username='Ali';")
    count = cursor.fetchall()
    assert len(count) == 1, "Aynı kullanıcı adıyla birden fazla kullanıcı eklenmemelidir."

def test_authenticate_user_success(setup_database):
    """Başarılı kullanıcı doğrulamasını test eder."""
    add_user("Veli", "veli@example.com", "password123")
    assert authenticate_user("Veli", "password123") is True, "Doğru kullanıcı adı ve şifre ile doğrulama başarılı olmalıdır."

def test_authenticate_user_nonexistent(setup_database):
    """Var olmayan bir kullanıcıyla doğrulama yapmayı test eder."""
    assert authenticate_user("NonExistentUser", "somepassword") is False, "Var olmayan kullanıcıyla doğrulama başarısız olmalıdır."

def test_authenticate_user_wrong_password(setup_database):
    """Yanlış şifreyle doğrulama yapmayı test eder."""
    add_user("Mehmet", "email@gmail.com", "correctpassword")
    assert authenticate_user("Mehmet", "wrongpassword") is False, "Yanlış şifreyle doğrulama başarısız olmalıdır."

