import httpx

from contra import settings
from urllib import response



async def get_access_token() -> str:
    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'en_US',
        'Content-Type': 'application/json',
    }
    auth = (settings.PAYPAL_CLIENT_ID, settings.PAYPAL_SECRET_ID)
    data = {'grant_type': 'client_credentials'}

    async with httpx.AsyncClient() as client:
        resp_data = (await client.post(
            settings.PAYPAL_AUTH_URL,
            auth = auth,
            headers = headers,
            data = data,
        )).json()
        return resp_data['access_token']
    
async def update_subscription_pp(
    acess_token: str,
    subscription_id: str,
    new_plan_id: str,
    return_url: str,
    cancel_url: str,
) -> str:
    
    url = f"{settings.PAYPAL_BILLING_SUBSCRIPTIONS_URL}/v1/billing/subscriptions/{subscription_id}/revise"
    
    bearer_token = f"Bearer {acess_token}"

    headers = {
        "Content-Type": "application/json",
        "Authorization": bearer_token,
        "Accept": "application/json",
    }
    
    update_data = {
        "plan_id": new_plan_id,
        "application_context": {
            "return_url": return_url,
            "cancel_url": cancel_url,
            "user_action": "SUBSCRIBE_NOW",
        },
    }
    
    approval_url = ""
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=update_data)

        print(f"{response.status_code=}")
        
        response_json = response.json()
        
        for link in response_json.get("links"):
            if link.get("rel") == "approve":
                approval_url = link["href"]
                break
        
    return approval_url


async def cancel_subscription(
    access_token: str,
    subscription_id: str,
    reason = 'Not specified',
):
    bearer_token = f'Bearer {access_token}'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': bearer_token,
        'Accept': 'application/json',
    }
    url = f'{settings.PAYPAL_BILLING_SUBSCRIPTIONS_URL}/{subscription_id}/cancel'
    data = { 'reason': reason }
    async with httpx.AsyncClient() as client:
        resp = (await client.post(url, headers=headers))
        print(f'[+] {resp.status_code}')