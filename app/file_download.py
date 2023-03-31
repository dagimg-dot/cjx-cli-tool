import aiohttp
from tqdm import tqdm
import os
import asyncio
import requests
from animator import Animator

class FileDownloader:
    async def get_release(self):
        async with aiohttp.ClientSession() as session:
            url = f"https://api.github.com/repos/dagimg-dot/cjx-cli-tool/releases/latest"
            try:
                async with session.get(url) as response:
                    response_json = await response.json()
                    return response_json
            except aiohttp.ClientError as error:
                print(f"Error occurred while making request: {error}")

    async def get_file_size(self,url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                file_size = int(response.headers.get('Content-Length', 0))
                return file_size


    async def check_version(self):
        response_j = await self.get_release()
        latest_version = response_j["tag_name"]
        current_version = "v2.1"
        if latest_version != current_version:
            print(
                f"A new version ({latest_version}) is available !")
            await self.zip_download(response_j,latest_version)
        else:
            print(
                f"You are using the latest version ({latest_version}).")
            
    async def zip_download(self, response_j ,latest_version):
        asset_url = response_j["assets"][0]["browser_download_url"]
        print_stat = f"{'Downloading the latest release ({}) : size => ':<30}".format(latest_version)
        try:
            total_size =  await Animator.animator(self.get_file_size,print_stat,asset_url)
        except KeyboardInterrupt as e:
            print(f"{'Cancelled by the user':<60}")
            return
        block_size = 1024

        total_size_MB = round(total_size/(1000*1000),ndigits=3)
        print(f"{print_stat} {total_size_MB} MB")

        try:
            if os.path.exists("myfile.zip"):
                os.remove("myfile.zip")

            response = requests.get(asset_url, stream = True)
            with open("myfile.zip", "wb") as f:
                with tqdm(total=total_size, unit="B", unit_scale=True, miniters=1,colour= 'green') as pbar:
                    for data in response.iter_content(block_size):
                        pbar.update(len(data))
                        f.write(data)

            print("\nDownload complete")
        except KeyboardInterrupt as e:
            pass

            

fd = FileDownloader()
try:
    print_stat = f"{'Checking latest release':<25}"
    asyncio.run(Animator.animator(fd.check_version,print_stat,None))
except KeyboardInterrupt:
    print(f"{'Cancelled by the user':<60}")
    