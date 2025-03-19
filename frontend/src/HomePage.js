import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";

function HomePage(){
    const navigate = useNavigate();
    const [query, setquery] = useState("")// State to hold the search query

    const search = async (e) => {
        e.preventDefault();
        navigate('/search/'+query);
    }

    return(
        <div>
            <form onSubmit={search}> 
                <input type="text" value={query} onChange={(e) => setquery(e.target.value)}></input>
                <button type="submit">Search</button>
            </form>
        </div>
    )
} export default HomePage;