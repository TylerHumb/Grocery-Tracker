import { useEffect, useState } from 'react';
import {useParams} from 'react-router-dom'
import { useNavigate } from "react-router-dom";
function Search(){
    const navigate = useNavigate();
    const { query } = useParams(); //get the search query from the URL
    const [results, setresults] = useState("")// State to hold the search query
    
    const navigateProdcut = async (id) => {
        navigate('/product/'+id);
    }
    // fetch search results once page loads
    useEffect(() => {
        const fetchresults = async () => {
            try {
                const response = await fetch(`http://localhost:8080/products/search/${query}`);
                if (!response.ok){
                    throw new Error("error during search");
                }
                const searchResults = await response.json();
                setresults(searchResults);
                console.log(results)
            } catch (error) {
                console.log(error.message)
            }
        };
        fetchresults(); // call fetchresults
    },[query]); //calls when query changes
    return (
        <div>
          <h1>Search Results for "{query}"</h1>
          <div>
            {/* Check if there are any results */}
            {Object.keys(results).length === 0 ? (
              <p>No results found.</p>
            ) : (
              Object.entries(results).map(([productName, productDetails]) => (
                <div key={productName} className="product-item" onClick={() =>navigateProdcut(productDetails.ProductID)}>
                  <h2>{productName}</h2>
                  {/* Check if productDetails is null or undefined */}
                  {!productDetails ? (
                    <p>N/A</p>
                  ) : (
                    <div>
                      <p>Price: ${productDetails.Price}</p>
                      <p>Last Updated: {productDetails.Date}</p>
                    </div>
                  )}
                </div>
              ))
            )}
          </div>
        </div>
      );
    }
    
    export default Search;