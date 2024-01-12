#SingleInstance Force

F2::ExitApp

F1::

; Set the range of time in milliseconds
MinTime := 70000 ; 45s 
MaxTime := 90000 ; 90s

; Generate a random time within the specified range
Random, RandomTime, %MinTime%, %MaxTime%

; ANIMALS
PromptArray := ["A dynamic image of a gazelle herd running across the African grasslands."]
PromptArray.Push("A powerful image of a lion in its natural habitat, showcasing its regal presence and the untamed beauty of the animal kingdom.")
PromptArray.Push("An underwater scene featuring a vibrant coral reef and a variety of tropical fish, highlighting the biodiversity of marine life.")
PromptArray.Push("A close-up shot of a red fox in a forest clearing, expressing curiosity and showcasing the grace of a wild mammal.")
PromptArray.Push("A heartwarming scene of a family of elephants in the African savannah, emphasizing the bond between these gentle giants.")
PromptArray.Push("A dynamic shot of dolphins leaping out of the water, capturing their playful and energetic behavior in their natural aquatic environment.")
PromptArray.Push("A captivating image of a colony of penguins in Antarctica, huddling together for warmth and emphasizing the harsh conditions of the polar region.")
PromptArray.Push("A colorful display of butterflies resting on a bed of vibrant flowers, illustrating the delicate and intricate beauty of these winged creatures.")
PromptArray.Push("A picturesque scene of giraffes grazing in the African grasslands, showcasing the elegance of these long-necked herbivores.")
PromptArray.Push("Adorable red pandas playing and climbing in treetops, highlighting the charm and agility of these endangered animals.")
PromptArray.Push("A serene coastal scene with a flock of seagulls in flight, capturing the freedom and grace of seabirds over the ocean.")
PromptArray.Push("A majestic moment of a whale breaching the ocean surface, showcasing the immense power and beauty of these marine giants.")
PromptArray.Push("An intimate scene of a chimpanzee family bonding, expressing emotions and relationships within the primate community.")
PromptArray.Push("An action shot of a cheetah in full sprint across the savannah, emphasizing the speed and agility of the world's fastest land mammal.")
PromptArray.Push("A vibrant display of macaws perched in the rainforest, showcasing the brilliant colors of these tropical parrots.")
PromptArray.Push("A majestic eagle soaring against a backdrop of mountainous landscapes, symbolizing freedom and mastery of the skies.")
PromptArray.Push("An underwater view of a diverse school of tropical fish swimming through a coral reef, displaying the harmony of marine ecosystems.")
PromptArray.Push("A cute sloth hanging from a tree branch in the rainforest canopy, embodying the slow and relaxed nature of these arboreal mammals.")
PromptArray.Push("A heartening sight of an African elephant enjoying a bath in a watering hole, demonstrating the intelligent and social nature of these giants.")
PromptArray.Push("A delightful scene of otters playing and splashing in a river, illustrating the playful behavior of these aquatic mammals.")
PromptArray.Push("A captivating moment of a humpback whale lifting its massive tail out of the water, showcasing their unique behavior in the ocean.")
PromptArray.Push("Adorable cheetah cubs observing and learning hunting skills from their mother, emphasizing the nurturing aspect of wild cat families.")
PromptArray.Push("A breathtaking image of a cluster of monarch butterflies during their migration, highlighting the extraordinary journey of these delicate insects.")
PromptArray.Push("A group of Gentoo penguins navigating the icy terrain of Antarctica, showcasing their resilience and adaptability to extreme environments.")
PromptArray.Push("A close-up shot of a hummingbird feeding on the nectar of a flower, capturing the rapid wing beats and vibrant colors of these tiny avian wonders.")
PromptArray.Push("A serene scene of a tiger resting in a sunlit clearing, demonstrating the elusive and powerful nature of these apex predators.")
PromptArray.Push("A picturesque view of a family of giraffes peacefully grazing under the shade of acacia trees, showcasing the elegance of these long-necked mammals.")
PromptArray.Push("An endearing image of a hedgehog curled up in a meadow, highlighting the charming and spiky nature of these nocturnal creatures.")
PromptArray.Push("A captivating scene of a pod of orcas swimming in the open ocean, illustrating the social bonds and intelligence of these marine mammals.")
PromptArray.Push("A heartwarming moment of a kangaroo joey peeking out from its mother's pouch, symbolizing maternal care in marsupials.")
PromptArray.Push("An intimate moment of an albatross pair engaging in a courtship display, demonstrating the elaborate rituals of these seabirds.")
PromptArray.Push("A stealthy black panther camouflaged amidst lush jungle foliage, embodying the elusive and mysterious nature of these big cats.")
PromptArray.Push("A serene image of a flock of flamingos wading in shallow waters, showcasing the vibrant pink hues and elegance of these water birds.")
PromptArray.Push("An adorable koala clinging to a eucalyptus tree branch, highlighting their arboreal lifestyle and affinity for eucalyptus leaves.")
PromptArray.Push("A vibrant red-eyed tree frog perched on a leaf in a tropical rainforest, showcasing the vivid colors of amphibians in their natural habitat.")
PromptArray.Push("A cheetah lounging on a termite mound, blending with the savannah landscape and exemplifying the cat's vigilant nature.")
PromptArray.Push("A touching scene of a polar bear mother and her cubs on an ice floe, highlighting the maternal bonds in the challenging Arctic environment.")
PromptArray.Push("A playful image of dolphins engaged in synchronized swimming, showcasing their intelligence and social interactions in the marine world.")
PromptArray.Push("A close-up of a vibrant toucan perched on a tree branch, displaying the distinctive and colorful beak of these tropical birds.")
PromptArray.Push("A powerful grizzly bear fishing in a rocky stream, capturing the bear's strength and prowess in catching salmon during the annual migration.")
PromptArray.Push("An endearing moment of a chimpanzee mother cuddling her baby, illustrating the close familial bonds within primate communities.")
PromptArray.Push("A mesmerizing scene of a monarch butterfly emerging from its chrysalis, symbolizing metamorphosis and the cycle of life.")
PromptArray.Push("A heartening view of an elephant herd gathered at a watering hole, emphasizing the social structure and communal behavior of these gentle giants.")
PromptArray.Push("A white Arctic fox blending into its snowy surroundings, showcasing its winter camouflage adaptation in the Arctic tundra.")
PromptArray.Push("A group of lemurs navigating through the lush forests of Madagascar, highlighting the unique biodiversity of the island.")
PromptArray.Push("A playful group of sea otters floating among kelp in a coastal kelp forest, illustrating the otters' agile and buoyant nature.")
PromptArray.Push("A majestic eagle owl perched on a branch in a moonlit forest, capturing the mystical and nocturnal essence of these large owls.")
PromptArray.Push("A mesmerizing underwater scene of manta rays gracefully gliding through the ocean, showcasing their majestic movements.")
PromptArray.Push("A charming view of puffins nesting on a clifftop, symbolizing the bustling activity during the breeding season in seabird colonies.")
PromptArray.Push("A dynamic image of a gazelle herd running across the African grasslands, illustrating the agility and speed of these graceful herbivores.")
PromptArray.Push("A heartwarming scene of a harbor seal pup resting on a rocky shore, showcasing the vulnerability and cuteness of young marine mammals.")
PromptArray.Push("A wise owl family making their home in the hollow of an ancient oak tree, surrounded by dappled sunlight filtering through the leaves.")
PromptArray.Push("Resourceful urban foxes navigating city streets under the glow of streetlights, adapting to life in an urban environment.")
PromptArray.Push("A group of pelicans flying in perfect formation over a serene lake, their wings reflecting in the still waters below.")
PromptArray.Push("Wild mustangs grazing freely on expansive grasslands, capturing the untamed beauty of these iconic North American horses.")
PromptArray.Push("A colony of penguins gathering on a pebble-strewn shoreline, exemplifying the organized chaos of their communal nesting grounds.")
PromptArray.Push("A family of deer gracefully moving through a sunlit glade in a peaceful forest setting, embodying the tranquility of the wilderness.")
PromptArray.Push("A friendly golden retriever serving as an honorary lifeguard on a sandy beach, watching over beachgoers with a vigilant gaze.")
PromptArray.Push("Playful monkeys relishing a feast of tropical fruits, showcasing their social interactions and resourcefulness in a lush jungle.")
PromptArray.Push("Harbor seals sunbathing on rocky coastal outcrops, blending seamlessly into their natural environment as they rest by the sea.")
PromptArray.Push("Inquisitive lemurs exploring a bamboo grove, their wide-eyed curiosity capturing the charm of these Madagascar natives.")
PromptArray.Push("A diligent squirrel collecting acorns amidst autumn foliage in a city park, adapting its natural behaviors to an urban landscape.")
PromptArray.Push("A kangaroo mother providing a cozy nap spot for her joey in the safety of her pouch, a heartwarming scene in the Australian Outback.")
PromptArray.Push("A monogamous pair of albatross engaged in an elaborate courtship display, reinforcing their lifelong bonds in the open ocean.")
PromptArray.Push("Energetic cheetah cubs playfully wrestling on the sunlit savannah, honing their hunting skills in a delightful manner.")
PromptArray.Push("A hummingbird delicately sipping nectar from vibrant blossoms, showcasing the precision and agility of these tiny avian wonders.")
PromptArray.Push("An armadillo curled up in the shade of a desert plant, seeking refuge from the sun while displaying its distinctive armored shell.")
PromptArray.Push("A herd of gentle elephants bathing and splashing in a jungle river, enjoying a communal moment of relaxation.")
PromptArray.Push("Adorable red panda duo climbing and exploring the treetops, their fluffy tails adding a touch of charm to the forest canopy.")
PromptArray.Push("A massive whale shark gracefully gliding through crystal-clear ocean waters, emphasizing the beauty of these gentle giants.")
PromptArray.Push("A majestic bald eagle perched on a rocky cliff, surveying its surroundings with a watchful gaze in a natural wilderness setting.")
PromptArray.Push("Playful otters floating down a gentle stream, reveling in the joy of aquatic adventures within a pristine natural habitat.")
PromptArray.Push("An Arctic hare blending seamlessly into the snowy tundra, showcasing its winter coat adaptation in the Arctic wilderness.")
PromptArray.Push("Graceful giraffes silhouetted against a vibrant sunset, their distinctive profiles adding elegance to the African savannah.")
PromptArray.Push("Raccoons exploring an urban backyard with a mix of curiosity and caution, adapting to coexist with human environments.")
PromptArray.Push("A border collie showcasing its intelligence and agility while navigating an obstacle course, capturing the dynamic energy of a working dog.")
PromptArray.Push("An elusive aardvark foraging for termites in the African grasslands, its unique appearance highlighted in the soft glow of dawn.")
PromptArray.Push("A family of quokkas, often called the happiest animals, basking in the warm Australian sun, showcasing their friendly and smiling faces.")
PromptArray.Push("A numbat, also known as the banded anteater, skillfully gathering termites in its woodland habitat, emphasizing its insect-eating behavior.")
PromptArray.Push("An axolotl, a unique aquatic salamander, swimming in a colorful enclosure, displaying its regenerative abilities and vibrant appearance.")
PromptArray.Push("A fossa, a cat-like carnivore native to Madagascar, stealthily hunting in the dense rainforest, its long body and sharp features in focus.")
PromptArray.Push("A jerboa, a small rodent with long hind legs, leaping across desert sand dunes, showcasing its remarkable agility and adaptations.")
PromptArray.Push("An okapi, the elusive forest giraffe, grazing among lush vegetation in the central African rainforest, its striking coat visible through the foliage.")
PromptArray.Push("A quoll, a carnivorous marsupial, prowling through the Australian bush at night, its distinctive spotted fur illuminated by moonlight.")
PromptArray.Push("A blobfish, residing in the deep-sea habitat, its unique gelatinous appearance adapted to the extreme pressures of the ocean depths.")
PromptArray.Push("A leaf-tailed gecko perfectly camouflaged against tree bark in Madagascar, showcasing its leaf-like appearance for effective camouflage.")
PromptArray.Push("A fishing cat wading through Southeast Asian wetlands, showcasing its unique aquatic adaptations for hunting and fishing.")
PromptArray.Push("A hagfish, known for its slimy defensive mechanism, coiling on the ocean floor, highlighting its primitive but fascinating features.")
PromptArray.Push("A markhor, a wild goat with spiral horns, navigating the rocky terrain of mountainous regions, showcasing its adaptability to harsh environments.")
PromptArray.Push("Nudibranchs, vibrant sea slugs, adding a burst of color to a coral reef, showcasing the diversity of marine life in tropical waters.")
PromptArray.Push("An aye-aye, a nocturnal primate, foraging for insects in the dense forests of Madagascar, showcasing its distinctive elongated middle finger.")
PromptArray.Push("A mantis shrimp, with its vibrant colors and powerful appendages, dwelling in shallow coral waters, highlighting its unique anatomy.")
PromptArray.Push("A gaur, the largest wild cattle species, roaming freely in the dense forests of Southeast Asia, emphasizing its massive build.")
PromptArray.Push("A transparent glass frog perched on a rainforest leaf, its see-through skin revealing internal organs, showcasing this amphibian's unique anatomy.")
PromptArray.Push("A cacomistle, also known as a ringtail, resting in the canopy of Central American forests, displaying its long, ringed tail.")
PromptArray.Push("A star-nosed mole, known for its unique fleshy appendages, burrowing in the soil of Eastern North America, highlighting its specialized adaptations.")
PromptArray.Push("A coelacanth, a prehistoric fish species, swimming in the dark depths of the ocean abyss, emphasizing its living fossil status.")
PromptArray.Push("A pack of dholes, or Asiatic wild dogs, hunting in the grasslands of India, showcasing their cooperative and social hunting behaviors.")
PromptArray.Push("A red panda navigating the Himalayan forest canopy, its fluffy tail and reddish fur blending seamlessly with the lush vegetation.")
PromptArray.Push("A pod of narwhals, known for their long tusks, migrating through Arctic waters, showcasing their distinctive and mysterious presence.")
PromptArray.Push("A tufted puffin nesting on rocky cliffs in coastal regions, its vibrant beak and tufted feathers adding charm to its nesting site.")



ArrayIndex := 1
Loop
{
    PromptSize := PromptArray.Length()
    
    Loop, %PromptSize%
    {
        Prompt := PromptArray[ArrayIndex]
        ArrayIndex := ArrayIndex + 1
        
        Click, Left
        SendInput, /imagine
        Sleep, 500
        SendInput, {Enter}
        Sleep, 300 
        SendInput, %Prompt%
        Sleep, 300  ; delay to ensure the paste window appears
        SendInput, {Space}
        Sleep, 200  ; delay to ensure the paste window appears
        SendInput, full screen, sharp focus, stock image, 8k, ultra hd, ultra realistic, 
        SendInput, in the style of realistic hyper-detailed, topcor 58mm f/1.4 --ar 16:9 --c 30
        Sleep, 500  ; delay to ensure the paste window appears
        Send, {Enter}

        if (ArrayIndex > PromptSize){
            ArrayIndex := 1
        }
        Sleep, %RandomTime% 
    }
}
return
