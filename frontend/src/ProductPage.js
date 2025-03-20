import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';

function ProductPage() {
    const { productid } = useParams(); // Get product ID from the URL
    const [productDetails, setDetails] = useState(null);
    const [priceDetails, setPrice] = useState([]);

    useEffect(() => {
        const fetchResults = async () => {
            try {
                // Fetch product details
                const response = await fetch(`http://localhost:8080/products/${productid}`);
                if (!response.ok) {
                    throw new Error("Error retrieving product details");
                }
                const productData = await response.json();
                setDetails(productData);

                // Fetch price history
                const priceResponse = await fetch(`http://localhost:8080/products/allprice/${productid}`);
                if (!priceResponse.ok) {
                    throw new Error("Error retrieving prices");
                }
                const productPrices = await priceResponse.json();
                setPrice(productPrices);

            } catch (error) {
                console.log(error.message);
            }
        };

        fetchResults(); // Call function on mount or when `productid` changes
    }, [productid]);

    return (
        <div>
            <h2>{productDetails ? productDetails.Name : "Loading..."}</h2>
            <img 
                src={`https://cdn0.woolworths.media/content/wowproductimages/medium/${productid}.jpg`} 
            />
            <p>------------------------------------------------------------------------------------------------</p>
            <h3>Price History</h3>
            <ul>
                {priceDetails.length > 0 ? (
                    priceDetails.map((price, index) => (
                        <li key={index}>
                            ${price.Price} - {price.Date}
                        </li>
                    ))
                ) : (
                    <li>No price history available</li>
                )}
            </ul>
        </div>
    );
}

export default ProductPage;