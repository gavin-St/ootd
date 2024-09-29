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

interface DetectedArea {
  coords: number[][];
  items: ClothingItem[];
}

const sampleDetectedAreas: DetectedArea[] = [
  {
    coords: [
      [10, 10],
      [150, 10],
      [150, 200],
      [10, 200],
    ],
    items: [
      {
        type: "Jacket",
        color: "Blue",
        brand: "Levi's",
        style: "Denim",
        material: "Cotton",
        features: { distressed: true, buttons: 6 },
        additionalClothingProperties: ["Vintage wash", "Slim fit"],
        price: 89.99,
        purchaseLink: "https://example.com/denim-jacket",
        imageUrl: "/placeholder.svg?height=200&width=200",
      },
      {
        type: "Jacket",
        color: "Navy",
        brand: "Gap",
        style: "Bomber",
        material: "Polyester",
        features: { zippered: true, pockets: 4 },
        additionalClothingProperties: ["Water-resistant", "Lightweight"],
        price: 79.99,
        purchaseLink: "https://example.com/bomber-jacket",
        imageUrl: "/placeholder.svg?height=200&width=200",
      },
    ],
  },
  {
    coords: [
      [160, 100],
      [300, 100],
      [280, 250],
      [180, 250],
    ],
    items: [
      {
        type: "Shirt",
        color: "White",
        brand: "H&M",
        style: "T-Shirt",
        material: "Cotton",
        features: { crewneck: true, "short-sleeved": true },
        additionalClothingProperties: ["Regular fit", "Breathable fabric"],
        price: 24.99,
        purchaseLink: "https://example.com/white-tshirt",
        imageUrl: "/placeholder.svg?height=200&width=200",
      },
    ],
  },
  {
    coords: [
      [100, 300],
      [250, 300],
      [240, 500],
      [110, 500],
    ],
    items: [
      {
        type: "Pants",
        color: "Black",
        brand: "Zara",
        style: "Skinny Jeans",
        material: "Denim",
        features: { "high-waisted": true, "zip-fly": true },
        additionalClothingProperties: ["Stretch fabric", "Ankle length"],
        price: 69.99,
        purchaseLink: "https://example.com/black-jeans",
        imageUrl: "/placeholder.svg?height=200&width=200",
      },
    ],
  },
];

export default function EnhancedOutfitDashboard() {
  const [image, setImage] = useState<string | null>(null);
  const [fileImage, setFileImage] = useState<any>();
  const [hoveredArea, setHoveredArea] = useState<DetectedArea | null>(null);
  const [clickedArea, setClickedArea] = useState<DetectedArea | null>(null);
  const [selectedItemIndex, setSelectedItemIndex] = useState(0);
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [clickCoordinates, setClickCoordinates] = useState<
    [number, number] | null
  >(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const detailsCardRef = useRef<HTMLDivElement>(null);
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

  const handleAreaHover = (area: DetectedArea | null) => {
    if (!clickedArea) {
      setHoveredArea(area);
      setSelectedItemIndex(0);
    }
  };

  const handleAreaClick = (area: DetectedArea) => {
    setClickedArea(area);
    setHoveredArea(null);
    setSelectedItemIndex(0);
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
    console.log(fileImage)

    const apiUrl = `http://127.0.0.1:5000/?x=${x}&y=${y}`;

    const response = await fetch(apiUrl, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error("API request failed");
    }

    const data = await response.json();
    console.log(data);
  };

  const toggleDarkMode = () => {
    setIsDarkMode(!isDarkMode);
  };

  const activeArea = clickedArea || hoveredArea;

  const getEdgePoint = (points: number[][]) => {
    const x = points.map((p) => p[0]);
    const y = points.map((p) => p[1]);
    const maxX = Math.max(...x);
    const minY = Math.min(...y);
    return [maxX, minY];
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
                  <svg className="absolute top-0 left-0 w-full h-full">
                    {sampleDetectedAreas.map((area, index) => (
                      <polygon
                        key={index}
                        points={area.coords
                          .map((point) => point.join(","))
                          .join(" ")}
                        fill="rgba(255, 255, 255, 0.2)"
                        stroke={activeArea === area ? "red" : "white"}
                        strokeWidth="2"
                        onMouseEnter={() => handleAreaHover(area)}
                        onMouseLeave={() => handleAreaHover(null)}
                        onClick={() => handleAreaClick(area)}
                        style={{ cursor: "pointer" }}
                      />
                    ))}
                    {activeArea && detailsCardRef.current && (
                      <line
                        x1={getEdgePoint(activeArea.coords)[0]}
                        y1={getEdgePoint(activeArea.coords)[1]}
                        x2={
                          detailsCardRef.current.getBoundingClientRect().left -
                          16
                        }
                        y2={
                          detailsCardRef.current.getBoundingClientRect().top +
                          20
                        }
                        stroke="red"
                        strokeWidth="2"
                      />
                    )}
                  </svg>
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
          <Card
            className="w-full lg:w-96 dark:bg-gray-800"
            ref={detailsCardRef}
          >
            <CardContent className="p-4">
              <h2 className="text-2xl font-semibold mb-4 dark:text-white">
                Item Details
              </h2>
              {activeArea ? (
                <Tabs defaultValue="0" className="w-full">
                  <TabsList className="grid w-full grid-cols-2 mb-4">
                    {activeArea.items.map((_, index) => (
                      <TabsTrigger
                        key={index}
                        value={index.toString()}
                        onClick={() => setSelectedItemIndex(index)}
                      >
                        Item {index + 1}
                      </TabsTrigger>
                    ))}
                  </TabsList>
                  {activeArea.items.map((item, index) => (
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
                  Click or hover over an item to see details
                </p>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
