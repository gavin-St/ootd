import { useState, useRef, useEffect } from "react";
import Image from "next/image";
import { Upload, ShoppingBag, Sun, Moon } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Badge } from "@/components/ui/badge";

interface ClothingFeature {
  [key: string]: string | number | boolean;
}

interface ClothingItem {
  type:
    | "Shoes"
    | "Jacket"
    | "Shirt"
    | "Pants"
    | "Dress"
    | "Hat"
    | "Glasses"
    | "Chain"
    | "Sweater"
    | "Skirt";
  color: string;
  brand: string;
  style: string;
  material: string;
  features: ClothingFeature;
  additionalClothingProperties: string[];
  price: number;
  purchaseLink: string;
  imageUrl: string;
}

export default function EnhancedOutfitDashboard() {
  const [image, setImage] = useState<string | null>(null);
  const [fileImage, setFileImage] = useState<any>();
  const [selectedItemIndex, setSelectedItemIndex] = useState(0);
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [clickCoordinates, setClickCoordinates] = useState<
    [number, number] | null
  >(null);
  const [items, setItems] = useState<ClothingItem[]>([]);

  const fileInputRef = useRef<HTMLInputElement>(null);
  const uploadedImageRef = useRef<HTMLDivElement>(null);
  const imageRef = useRef<HTMLImageElement>(null);

  useEffect(() => {
    const root = window.document.documentElement;
    root.classList.toggle("dark", isDarkMode);
  }, [isDarkMode]);

  const handleImageUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => setImage(e.target?.result as string);
      reader.readAsDataURL(file);
      setFileImage(file);
    }
  };

  const handleImageClick = (event: React.MouseEvent<HTMLDivElement>) => {
    if (!uploadedImageRef.current || !imageRef.current) return;

    const rect = uploadedImageRef.current.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;

    const displayedImageWidth = imageRef.current.offsetWidth;
    const displayedImageHeight = imageRef.current.offsetHeight;

    const originalImageWidth = imageRef.current.naturalWidth;
    const originalImageHeight = imageRef.current.naturalHeight;

    const xScale = originalImageWidth / displayedImageWidth;
    const yScale = originalImageHeight / displayedImageHeight;

    const adjustedX = x * xScale;
    const adjustedY = y * yScale;

    setClickCoordinates([adjustedX, adjustedY]);

    sendApiRequest(adjustedX, adjustedY);
  };

  const sendApiRequest = async (x: number, y: number) => {
    if (!fileImage) return;
    const formData = new FormData();

    formData.append("file", fileImage);

    const apiUrl = `http://127.0.0.1:5000/?x=${x}&y=${y}`;

    const response = await fetch(apiUrl, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error("API request failed");
    }

    const data = await response.json();

    const processedItems = processApiResponse(data);
    setItems(processedItems);
    setSelectedItemIndex(0);
  };

  const processApiResponse = (data: any[]): ClothingItem[] => {
    return data.map((item) => {
      const additionalClothingProperties: string[] = [];
      const featuresTemp: {
        [index: string]: { key: string; value: string };
      } = {};

      // Process additionalClothingProperties
      Object.keys(item).forEach((key) => {
        if (key.startsWith("additionalClothingProperties_")) {
          additionalClothingProperties.push(item[key]);
        }
        if (key.startsWith("features_")) {
          const match = key.match(/^features_(\d+)_(key|value)$/);
          if (match) {
            const index = match[1];
            const subkey = match[2]; // 'key' or 'value'
            if (!featuresTemp[index])
              featuresTemp[index] = { key: "", value: "" };
            featuresTemp[index][subkey] = item[key];
          }
        }
      });

      const featuresObj: ClothingFeature = {};
      Object.values(featuresTemp).forEach((feat) => {
        featuresObj[feat.key] = feat.value;
      });

      let price = parseFloat(item.price.replace("$", ""));

      return {
        type: item.type,
        color: item.color,
        brand: item.brand,
        style: item.style,
        material: item.material,
        features: featuresObj,
        additionalClothingProperties,
        price,
        purchaseLink: item.shoppingUrl,
        imageUrl: item.imgUrl,
      };
    });
  };

  const toggleDarkMode = () => {
    setIsDarkMode(!isDarkMode);
  };

  return (
    <div
      className={`min-h-screen ${isDarkMode ? "dark" : ""} dark:bg-gray-900`}
    >
      <div className="container mx-auto p-4 transition-colors duration-200">
        <div className="flex justify-between items-center mb-4">
          <h1 className="text-3xl font-bold dark:text-white">
            Outfit of the Day
          </h1>
          <Button variant="outline" size="icon" onClick={toggleDarkMode}>
            {isDarkMode ? (
              <Sun className="h-[1.2rem] w-[1.2rem]" />
            ) : (
              <Moon className="h-[1.2rem] w-[1.2rem]" />
            )}
          </Button>
        </div>
        <div className="flex flex-col lg:flex-row gap-4">
          <Card className="flex-1 dark:bg-gray-800">
            <CardContent className="p-4">
              {image ? (
                <div
                  ref={uploadedImageRef}
                  onClick={handleImageClick}
                  className="relative cursor-pointer"
                >
                  <Image
                    src={image}
                    alt="Uploaded outfit"
                    width={500}
                    height={500}
                    className="w-full h-auto rounded-lg"
                    ref={imageRef}
                  />
                </div>
              ) : (
                <div className="flex items-center justify-center h-64 bg-gray-100 dark:bg-gray-700 rounded-lg">
                  <Button onClick={() => fileInputRef.current?.click()}>
                    <Upload className="mr-2 h-4 w-4" /> Upload Image
                  </Button>
                  <input
                    type="file"
                    accept="image/*"
                    onChange={handleImageUpload}
                    className="hidden"
                    ref={fileInputRef}
                  />
                </div>
              )}
            </CardContent>
          </Card>
          <Card className="w-full lg:w-96 dark:bg-gray-800">
            <CardContent className="p-4">
              <h2 className="text-2xl font-semibold mb-4 dark:text-white">
                Item Details
              </h2>
              {items.length > 0 ? (
                <Tabs defaultValue="0" className="w-full">
                  <TabsList className="grid w-full grid-cols-3 mb-4">
                    {items.map((_, index) => (
                      <TabsTrigger
                        key={index}
                        value={index.toString()}
                        onClick={() => setSelectedItemIndex(index)}
                      >
                        Item {index + 1}
                      </TabsTrigger>
                    ))}
                  </TabsList>
                  {items.map((item, index) => (
                    <TabsContent key={index} value={index.toString()}>
                      <div className="space-y-4">
                        <div className="aspect-square overflow-hidden rounded-lg">
                          <Image
                            src={item.imageUrl}
                            alt={`${item.brand} ${item.type}`}
                            width={200}
                            height={200}
                            className="w-full h-full object-cover"
                          />
                        </div>
                        <div>
                          <h3 className="text-xl font-bold dark:text-white">
                            {item.type}
                          </h3>
                          <p className="text-gray-600 dark:text-gray-300">
                            {item.brand} - {item.style}
                          </p>
                        </div>
                        <div className="grid grid-cols-2 gap-2">
                          <Badge variant="secondary">{item.color}</Badge>
                          <Badge variant="secondary">{item.material}</Badge>
                        </div>
                        {Object.keys(item.features).length > 0 && (
                          <div>
                            <h4 className="font-semibold dark:text-white">
                              Features:
                            </h4>
                            <ul className="list-disc list-inside dark:text-gray-300">
                              {Object.entries(item.features).map(
                                ([key, value]) => (
                                  <li key={key}>
                                    {key}: {value.toString()}
                                  </li>
                                )
                              )}
                            </ul>
                          </div>
                        )}
                        {item.additionalClothingProperties.length > 0 && (
                          <div>
                            <h4 className="font-semibold dark:text-white">
                              Additional Properties:
                            </h4>
                            <ul className="list-disc list-inside dark:text-gray-300">
                              {item.additionalClothingProperties.map(
                                (prop, i) => (
                                  <li key={i}>{prop}</li>
                                )
                              )}
                            </ul>
                          </div>
                        )}
                        <div className="flex items-center justify-between">
                          <span className="text-2xl font-bold dark:text-white">
                            ${item.price.toFixed(2)}
                          </span>
                          <Button asChild>
                            <a
                              href={item.purchaseLink}
                              target="_blank"
                              rel="noopener noreferrer"
                            >
                              <ShoppingBag className="mr-2 h-4 w-4" /> Buy Now
                            </a>
                          </Button>
                        </div>
                      </div>
                    </TabsContent>
                  ))}
                </Tabs>
              ) : (
                <p className="text-gray-500 dark:text-gray-400">
                  Click on the image to get item details
                </p>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
