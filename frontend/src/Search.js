import {useParams} from 'react-router-dom'
function Search(){
    const { query } = useParams(); //get the search query from the URL


    return(
        <div>
            <p>You searched for {query}</p>
        </div>
    )

} export default Search;