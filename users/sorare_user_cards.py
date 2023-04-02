import aiohttp


class SorareCards:

    def __init__(self, x_algolia_api_key, x_algolia_application_id, userID):
        self.x_algolia_api_key = x_algolia_api_key
        self.x_algolia_application_id = x_algolia_application_id
        self.userID = userID

    async def _gettingCardsId(self, response: dict):
        cards = {'assetIds': [], 'ids': []}
        for page in response['results']:
            for id in page['hits']:
                current_id = id['objectID'].split(':')[1:][0]
                if 'assetId' in id['objectID']:
                    cards['assetIds'].append(current_id)
                else:
                    cards['ids'].append(current_id)
        return cards


class MBACards(SorareCards):

    async def get_algolia_cards_id(self):

        """
            Принимаю: x-algolia-api-key, x-algolia-application-id , userID
            Возвращаю: массив из ID всех карточек
        """

        url = 'https://7z0z8pasdy-dsn.algolia.net/1/indexes/*/queries'

        headers = {
            'x-algolia-api-key': self.x_algolia_api_key,
            'x-algolia-application-id': self.x_algolia_application_id
        }

        body = {"requests": [{"indexName": "Card",
                              "params": f"highlightPreTag=%3Cais-highlight-0000000000%3E&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&hitsPerPage=40&analyticsTags=%5B%22Gallery%22%5D&filters=sport%3Abaseball&distinct=true&attributesToRetrieve=%5B%22asset_id%22%5D&attributesToHighlight=none&maxValuesPerFacet=30&page=0&facets=%5B%22user.id%22%2C%22rarity%22%2C%22on_sale%22%2C%22position%22%2C%22grade%22%2C%22serial_number%22%2C%22team.long_name%22%2C%22player.display_name%22%2C%22player.birth_date_i%22%5D&tagFilters=&facetFilters=%5B%22user.id%3A{self.userID}%22%5D"}]}

        async with aiohttp.ClientSession() as session:
            response = await (await session.post(url, headers=headers, json=body, ssl=False)).json()

        cards = await self._gettingCardsId(response)

        PAGINATION = response['results'][0]['nbPages']
        for page in range(1, PAGINATION):
            loop_body = {"requests": [{"indexName": "Card",
                                       "params": f"highlightPreTag=%3Cais-highlight-0000000000%3E&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&hitsPerPage=40&analyticsTags=%5B%22Gallery%22%5D&filters=sport%3Abaseball&distinct=true&attributesToRetrieve=%5B%22asset_id%22%5D&attributesToHighlight=none&maxValuesPerFacet=30&page={page}&facets=%5B%22user.id%22%2C%22rarity%22%2C%22on_sale%22%2C%22position%22%2C%22grade%22%2C%22serial_number%22%2C%22team.long_name%22%2C%22player.display_name%22%2C%22player.birth_date_i%22%5D&tagFilters=&facetFilters=%5B%22user.id%3A{self.userID}%22%5D"}]}

            async with aiohttp.ClientSession() as session:
                loop_response = await (await session.post(url, headers=headers, json=loop_body, ssl=False)).json()

            current_cards = await self._gettingCardsId(loop_response)
            cards['assetIds'] += current_cards['assetIds']
            cards['ids'] += current_cards['ids']

        return cards

    async def getUserCards(self, assetIds: list, ids: list):
        """
            Принимаю массив из id карточек, возвращаю объект со всей инфой по карточкам
        """

        body = {
            "operationName": "CardsByIdsQuery",
            "variables": {
                "assetIds": assetIds,
                "ids": ids
            },
            "query": "query CardsByIdsQuery($assetIds: [String!]!, $ids: [String!]!) {\n  baseballCards(assetIds: $assetIds, ids: $ids) {\n    id\n    slug\n    assetId\n    ...MobileCardDetailsByAssetId_card\n    ...CommonCardPreview_BaseballCard\n    __typename\n  }\n}\n\nfragment CommonCardPreview_BaseballCard on BaseballCard {\n  id\n  slug\n  ...CardProperties_BaseballCard\n  ...CommonCardPreview_CardInterface\n  __typename\n}\n\nfragment CardProperties_BaseballCard on BaseballCard {\n  id\n  slug\n  assetId\n  totalBonus\n  seasonBonus\n  rarityBonus\n  xpBonus\n  bonusLossAfterTransfer\n  player {\n    slug\n    currentSeasonAverageScore {\n      pitching\n      batting\n      __typename\n    }\n    last15AverageScore {\n      pitching\n      batting\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment CommonCardPreview_CardInterface on CardInterface {\n  id\n  slug\n  ...ClickableCard_CardInterface\n  ...CardDescription_CardInterface\n  __typename\n}\n\nfragment ClickableCard_CardInterface on CardInterface {\n  slug\n  ...Card_CardInterface\n  __typename\n}\n\nfragment Card_CardInterface on CardInterface {\n  id\n  slug\n  fullImageUrl\n  player {\n    slug\n    displayName\n    __typename\n  }\n  __typename\n}\n\nfragment CardDescription_CardInterface on CardInterface {\n  id\n  slug\n  assetId\n  season\n  rarity\n  player {\n    slug\n    displayName\n    __typename\n  }\n  __typename\n}\n\nfragment MobileCardDetailsByAssetId_card on BaseballCard {\n  id\n  slug\n  positions\n  __typename\n}\n"
        }

        async with aiohttp.ClientSession() as session:
            cards = await session.post('https://api.sorare.com/sports/graphql',
                                       headers={'content-type': 'application/json'}, json=body, ssl=False)
            cards = (await cards.json())['data']

        return cards

    async def getCards(self):
        cardsID = await self.get_algolia_cards_id()
        cards = []

        countCards = max(len(cardsID['assetIds']), len(cardsID['ids']))
        for i in range(0, countCards, 40):
            currentCards = await self.getUserCards(cardsID['assetIds'][i:i + 40], cardsID['ids'][i:i + 40])
            cards += currentCards['baseballCards']

        return {"cards": cards}


class NBACards(SorareCards):

    async def get_algolia_cards_id(self):

        """
            Принимаю: x-algolia-api-key, x-algolia-application-id , userID
            Возвращаю: массив из ID всех карточек
        """

        url = 'https://7z0z8pasdy-dsn.algolia.net/1/indexes/*/queries'

        headers = {
            'x-algolia-api-key': self.x_algolia_api_key,
            'x-algolia-application-id': self.x_algolia_application_id
        }

        body = {"requests": [{"indexName": "Card",
                              "params": f"analyticsTags=%5B%22Gallery%22%5D&attributesToHighlight=%5B%5D&distinct=false&facets=%5B%22rarity%22%2C%22nba_stats.ten_game_average%22%2C%22grade%22%2C%22serial_number%22%2C%22team.long_name%22%2C%22player.display_name%22%2C%22player.birth_date_i%22%5D&filters=user.id%3A{self.userID}%20AND%20sport%3Anba&highlightPostTag=__%2Fais-highlight__&highlightPreTag=__ais-highlight__&hitsPerPage=40&maxValuesPerFacet=10&page=0&query=&tagFilters="}]}

        async with aiohttp.ClientSession() as session:
            response = await (await session.post(url, headers=headers, json=body, ssl=False)).json()

        cards = await self._gettingCardsId(response)

        PAGINATION = response['results'][0]['nbPages']
        for page in range(1, PAGINATION):
            loop_body = {"requests": [{"indexName": "Card",
                                       "params": f"analyticsTags=%5B%22Gallery%22%5D&attributesToHighlight=%5B%5D&distinct=false&facets=%5B%22rarity%22%2C%22nba_stats.ten_game_average%22%2C%22grade%22%2C%22serial_number%22%2C%22team.long_name%22%2C%22player.display_name%22%2C%22player.birth_date_i%22%5D&filters=user.id%3A{self.userID}%20AND%20sport%3Anba&highlightPostTag=__%2Fais-highlight__&highlightPreTag=__ais-highlight__&hitsPerPage=40&maxValuesPerFacet=10&page={page}&query=&tagFilters="}]}

            async with aiohttp.ClientSession() as session:
                loop_response = await (await session.post(url, headers=headers, json=loop_body, ssl=False)).json()

            current_cards = await self._gettingCardsId(loop_response)
            cards['assetIds'] += current_cards['assetIds']
            cards['ids'] += current_cards['ids']

        return cards

    async def getUserCards(self, assetIds: list, ids: list):
        """
            Принимаю массив из id карточек, возвращаю объект со всей инфой по карточкам
        """

        body = {
            "operationName": "NBACardsByIdsQuery",
            "variables": {
                "input": {
                    "assetIds": assetIds,
                    "ids": ids
                }
            },
            "query": "query NBACardsByIdsQuery($input: NBACardsInput!) {\n  nbaCards(input: $input) {\n    assetId\n    ...NBAMobileCardDetailsByAssetId_card\n    ...NBACommonCardPreview_NBACard\n    __typename\n  }\n}\n\nfragment NBACommonCardPreview_NBACard on NBACard {\n  id\n  ...NBACardProperties_NBACard\n  ...CommonCardPreview_CardInterface\n  __typename\n}\n\nfragment NBACardProperties_NBACard on NBACard {\n  id\n  assetId\n  totalBonus\n  seasonBonus\n  rarityBonus\n  xpBonus\n  bonusLossAfterTransfer\n  player {\n    tenGameAverage\n    ...IneligibleIndicator_NBAPlayer\n    __typename\n  }\n  __typename\n}\n\nfragment IneligibleIndicator_NBAPlayer on NBAPlayer {\n  slug\n  isActive\n  __typename\n}\n\nfragment CommonCardPreview_CardInterface on CardInterface {\n  id\n  ...ClickableCard_CardInterface\n  ...CardDescription_CardInterface\n  __typename\n}\n\nfragment ClickableCard_CardInterface on CardInterface {\n  ...Card_CardInterface\n  __typename\n}\n\nfragment Card_CardInterface on CardInterface {\n  id\n  slug\n  player {\n    slug\n    displayName\n    __typename\n  }\n  ...Card_CardParam\n  __typename\n}\n\nfragment Card_CardParam on CardInterface {\n  fullImageUrl\n  player {\n    displayName\n    __typename\n  }\n  __typename\n}\n\nfragment CardDescription_CardInterface on CardInterface {\n  id\n  assetId\n  season\n  rarity\n  player {\n    slug\n    displayName\n    __typename\n  }\n  __typename\n}\n\nfragment NBAMobileCardDetailsByAssetId_card on NBACard {\n  id\n  slug\n  positions\n  __typename\n}\n"
        }

        async with aiohttp.ClientSession() as session:
            cards = await session.post('https://api.sorare.com/sports/graphql',
                                       headers={'content-type': 'application/json'}, ssl=False, json=body)
            cards = (await cards.json())['data']

        return cards

    async def getCards(self):

        cardsID = await self.get_algolia_cards_id()
        cards = []

        countCards = max(len(cardsID['assetIds']), len(cardsID['ids']))
        for i in range(0, countCards, 40):
            currentCards = await self.getUserCards(cardsID['assetIds'][i:i + 40], cardsID['ids'][i:i + 40])
            cards += currentCards['nbaCards']

        return {"nbaCards": cards}
