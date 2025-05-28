def test_whatsapp_endpoint_greeting(client):
    resp = client.post(
        "/whatsapp/", data={"From": "whatsapp:+1", "Body": "Hola"})
    assert resp.status_code == 200
    assert resp.text.startswith("<?xml")
    assert "<Message>" in resp.text
