from datetime import datetime, timedelta

import pytest


@pytest.mark.django_db
def test_create_tracking(authorized_client):

    # test creating tracking with valid data
    valid_data = {
        "product_id": 123456,
        "tracking_interval": 24,
        "start_tracking_date": datetime.now(),
        "end_tracking_date": datetime.now() + timedelta(days=1)
    }

    response = authorized_client.post(
        path="/api/trackings/",
        data=valid_data,
        format="json"
    )

    assert response.status_code == 201, (
        "Make sure that response status code on request"
        "with valid data is 201. "
    )

    # test creating tracking with small tracking period
    invalid_data = {
        "product_id": 654321,
        "tracking_interval": 24,
        "start_tracking_date": datetime.now(),
        "end_tracking_date": datetime.now() + timedelta(hours=1)
    }

    response = authorized_client.post(
        path="/api/trackings/",
        data=invalid_data,
        format="json"
    )

    assert response.status_code == 400, (
        "Make sure that creating tracking with tracking period that is "
        "too small for this tracking interval is forbidden and "
        "400 status code is returned. "
    )

    # test uniquetogether validator
    response = authorized_client.post(
        path="/api/trackings/",
        data=valid_data,
        format="json"
    )

    assert response.status_code == 400, (
        "Make sure that user cannot create tracking with product_id "
        "which he is tracking yet. "
    )
