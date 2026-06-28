import aiohttp
from fastapi import HTTPException


async def fetch_html(url: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (GEO-Analyzer)"
    }

    try:
        # response = requests.get(url,headers=header, timeout=10)

        # 세션을 만들어서 api 요청
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url, timeout=10) as response:

                if response.status != 200:
                    raise HTTPException(
                        status_code=response.status,
                        detail=f"HTML 요청 실패 (코드: {response.status})"
                    )

                return await response.text()

    except aiohttp.ClientError as e:
        raise HTTPException(
            status_code=500,
            detail=f"요청 중 오류가 발생했습니다: {e}"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )