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
    
async def update_subscription_plan(
    acess_token: str,
    subscription_id: str,
    new_plan_id: str,
    return_url: str,
    cancel_url: str,
) -> str:
    
    url = f'{settings.PAYPAL_BILLING_SUBSCRIPTIONS_URL}/{subscription_id}/revise'
    
    headers = {
        'Authorization': f'Bearer {acess_token}',
        'Content-Type': 'application/json',
        'Accept': "application/json",
    }
    
    update_data = {
        'plan_id': new_plan_id,
        'application_context': {
            'return_url': return_url,
            'cancel_url': cancel_url,
            'user_action': 'SUBSCRIBE_NOW',
        },
    }
    
    approval_url = ""
    
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, headers=headers, json=update_data)
        resp.raise_for_status()

        print(f"[+]{resp.status_code=}")
        
        resp_data = resp.json()
        
        for link_details in resp_data.get('links', []):
            if link_details.get('rel') == 'approve':
                approval_url = link_details["href"]
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