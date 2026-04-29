#-*- coding: utf-8 -*-

import pytest

import sqlite3

from datetime import datetime, timezone

from backend.src.domain.models import EmailMessage, AnalysisResult

from backend.src.storage.database import Database



@pytest.fixture

def test_db(tmp_path):

    # SQLite ":memory:" kullanildiginda her baglanti kapandiginda tablolar silinir.

    # Bu yuzden pytest'in bize verdigi gecici bir dosya yolunu (tmp_path) kullaniyoruz.

    # Bu dosya test bittiginde otomatik silinir.

    db_file = tmp_path / "test_database.db"

    return Database(str(db_file))

#

def test_save_email_unicode_truncation(test_db):

    """

    BUG KONTROLU: Mail body_preview icin ilk 250 karakter aliniyor.

    Veritabani cokuyor mu test edelim.

    """

    long_emoji_body = "X" * 300

   

    email = EmailMessage(

        message_id="msg-emoji-1",

        sender="emoji@test.com",

        subject="Emojis",

        body=long_emoji_body,

        received_at=datetime.now(timezone.utc)

    )

   

    test_db.save_email(email)

   

    with test_db._connect() as conn:

        cursor = conn.execute("SELECT body_preview FROM emails WHERE message_id = 'msg-emoji-1'")

        row = cursor.fetchone()

       

        assert row is not None

        assert len(row[0]) <= 250



def test_duplicate_email_insert_ignore(test_db):

    """

    BUG KONTROLU: Ayni mail iki kere gelirse veritabani coker mi yoksa gormezden mi gelir?

    """

    email = EmailMessage(

        message_id="duplicate-id",

        sender="test@test.com",

        subject="Test",

        body="Test",

        received_at=datetime.now(timezone.utc)

    )

   

    test_db.save_email(email)

   

    try:

        test_db.save_email(email)

    except sqlite3.IntegrityError:

        pytest.fail("Veritabani duplicate kayitta coktu! INSERT OR IGNORE calismiyor.")