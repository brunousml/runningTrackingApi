from nose import with_setup


def _clean_store():
    import app
    app.views.STORE = {}


@with_setup(teardown=_clean_store)
def test_update_user_bad_variables():
    import app
    update = {
        'var1': 1552475073,
        'var2': 5560,
        'var3': 133910
    }
    username = 'john'
    with app.app.test_client() as client:
        res = client.post('/users/%s' % username, json=update)
        assert res.status_code == 400


@with_setup(teardown=_clean_store)
def test_create_user():
    import app
    update = {
        'ts': 1552475073,
        'distance': 5560,
        'time': 133910
    }
    username = 'john'
    with app.app.test_client() as client:
        res = client.post('/users/%s' % username, json=update)
        assert res.status_code == 200
        assert res.json.get('ts') == update.get('ts')
        assert res.json.get('cumulative_distance') == update.get('distance')
        assert res.json.get('cumulative_time') == update.get('time')
        assert res.json.get('user') == username


@with_setup(teardown=_clean_store)
def test_create_and_update_user():
    import app

    update_1 = {
        'ts': 1552475073,
        'distance': 5560,
        'time': 133910
    }
    update_2 = {
        'ts': 1552475073,
        'distance': 5560,
        'time': 133910
    }
    username = 'john'
    with app.app.test_client() as client:
        res = client.post('/users/%s' % username, json=update_1)
        assert res.status_code == 200
        res = client.patch('/users/%s' % username, json=update_2)
        assert res.status_code == 200

        assert res.json.get('ts') == update_2.get('ts')
        assert res.json.get('cumulative_distance') == update_1.get('distance') + update_2.get('distance')
        assert res.json.get('cumulative_time') == update_1.get('time') + update_2.get('time')
        assert res.json.get('user') == username


@with_setup(teardown=_clean_store)
def test_fetch_user():
    import app

    update = {
        'ts': 1552475073,
        'distance': 5560,
        'time': 133910
    }
    username = 'john'
    with app.app.test_client() as client:
        res = client.post('/users/%s' % username, json=update)
        assert res.status_code == 200
        res = client.get('/users/%s' % username)
        assert res.status_code == 200

        assert res.json.get('ts') == update.get('ts')
        assert res.json.get('cumulative_distance') == update.get('distance')
        assert res.json.get('cumulative_time') == update.get('time')
        assert res.json.get('user') == username


@with_setup(teardown=_clean_store)
def test_get_top_attributes():
    import app

    with app.app.test_client() as client:
        client.post('/users/john', json={
            'ts': 1552479093,
            'distance': 860,
            'time': 10910
        })
        client.post('/users/paul', json={
            'ts': 1552479093,
            'distance': 960,
            'time': 5910
        })
        client.post('/users/jenna', json={
            'ts': 1552479093,
            'distance': 1560,
            'time': 9910
        })

        res = client.get('/users/top/distance?size=2')
        assert res.status_code == 200
        assert len(res.json) == 2
        assert res.json[0]['user'] == 'jenna'
        assert res.json[0]['cumulative_distance'] == 1560
        assert res.json[1]['user'] == 'paul'
        assert res.json[1]['cumulative_distance'] == 960

        res = client.get('/users/top/time?size=2')
        assert res.status_code == 200
        assert len(res.json) == 2
        assert res.json[0]['user'] == 'john'
        assert res.json[0]['cumulative_time'] == 10910
        assert res.json[1]['user'] == 'jenna'
        assert res.json[1]['cumulative_time'] == 9910

        res = client.get('/users/top/speed?size=2')
        assert res.status_code == 200
        assert len(res.json) == 2
        assert res.json[0]['user'] == 'john'
        assert res.json[0]['cumulative_time'] == 10910
        assert res.json[1]['user'] == 'jenna'
        assert res.json[1]['cumulative_time'] == 9910


@with_setup(teardown=_clean_store)
def test_find_partner():
    import app

    with app.app.test_client() as client:
        client.post('/users/john', json={
            'ts': 1552479093,
            'distance': 860,
            'time': 10910
        })
        client.post('/users/paul', json={
            'ts': 1552479093,
            'distance': 960,
            'time': 5910
        })
        client.post('/users/jenna', json={
            'ts': 1552479093,
            'distance': 5459,
            'time': 13831
        })
        client.post('/users/michael', json={
            'ts': 1552479093,
            'distance': 3860,
            'time': 9910
        })
        client.post('/users/paula', json={
            'ts': 1552479093,
            'distance': 5560,
            'time': 12910
        })

        res = client.get('/users/paula/find-partners')
        assert res.status_code == 200
        assert res.json[0]['user'] == 'jenna'
        assert res.json[1]['user'] == 'michael'


@with_setup(teardown=_clean_store)
def test_private_route():
    import app

    with app.app.test_client() as client:
        client.post('/users/paul', json={
            'ts': 1552479093,
            'distance': 860,
            'time': 10910
        })

        res = client.get('/users/paul/private?token=pq72KttXvPNZWC7zdLANzUsQYwDd5H2s')
        assert res.status_code == 200
        assert res.json['user'] == 'paul'

        res = client.get('/users/paul/private?token=wrongToken')
        assert res.status_code == 401

        res = client.get('/users/jenna/private?token=pq72KttXvPNZWC7zdLANzUsQYwDd5H2s')
        assert res.status_code == 404

