FarmQuest Player Telemetry Dataset

This dataset comes with a datasheet for datasets. This is the (anonymous version)[Datasheets for Datasets_Anonymous.pdf] for review.

There are several types of events listed in the dataset. The class, type, value and description are all listed below. 
AS A NOTE: Timestamp data is unusable for this dataset as there was a problem with recording

| Class        | Type            | Value |  Description |
| ------------ | --------------  | ----- | ------------ |
| Event        | SessionStart   | None  | The player has started the game |
| Event        | Day             | <currentday>  | fires at the start of a new day and records <currentday> |
| QuestAlgorithm| Passage        | None  | Passage assigned as AI director |
| QuestAlgorithm| RLAID          | None  | RLAID assigned as AI director |
| QuestAlgorithm| Random         | None  | random assigned as AI director |
| Tansition     | Home           | None  | Player entered home level |
| Tansition     | Main           | None  | Player entered main level |
| Tansition     | QuestBoard     | None  | Player entered questboard level |
| Tansition     | Shop           | None  | Player entered shop level |
| Tansition     | TutorialQuestBoard| None  | Player entered tutorial questboard level |
| Tansition     | TutorialShop   | None  | Player entered tutorial shop level |
| Interaction   | Plant          | <plant>  | player planted a seed of type <plant> |
| Interaction   | HarvestCrop    | <plant>  | player harvested a fully grown crop of type <plant> |
| Interaction   | HarvestMushroom| None     | player harvested a mushroom |
| Interaction   | HarvestBerry   | None     | player harvested a berry|
| Interaction   | PlaceFurniture | <furniture>| player placed furniture <furniture> |
| Interaction   | RotateFurniture| <furniture>| player rotated furniture <furniture> |
| Interaction   | PickupFurniture| <furniture>| player picked up furniture <furniture> |
| Interaction   | Cook           | <recipe>  | player cooked a recipe of type <recipe> |
| Shop          | StartCoins     | <amount>  | player starts with <amount> of coins when they enter the shop|
| Shop          | Bought         | <item>    | player bought <item> from the shop|
| Shop          | TriedBought    | <item>    | player tried to buy <item> from the shop, but does not have enough money or does not have enough room in inventory|
| Shop          | Sold           | <item>    | player sold <item> to the shop|
| Shop          | Pay            | <amount>  | player paid <amount> to mortgage|
| Shop          | TriedPay       | <amount>  | player tried to pay <amount> to mortgage, but player does not have enough money or invalid amount entered|
| Shop          | AvailableFurniture| <item>    | furniture <item> is available for purchase at the shop|
| Shop          | AvailableSeed  | <item>    | seed <item> is available for purchase at the shop|
| Shop          | AvailableRecipe| <item>    | recipe <item> is available for purchase at the shop|
| Quest         | AvailableQuest| <name>    | Quest <name> was shown to the player as an option|
| Quest         | Accept        | <name>    | Player accepted quest <name>|
| Quest         | Submit        | <name>    | player submitted quest <name>|
| Quest         | Submit        | <name>    | player submitted quest <name>|
| QuestBoardState| Submit        | None     | Questboard is in state submit|
| QuestBoardState| accept        | None     | Questboard is in state accept|
