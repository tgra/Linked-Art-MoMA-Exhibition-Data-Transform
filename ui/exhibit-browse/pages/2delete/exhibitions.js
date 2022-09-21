import Head from 'next/head'
import Link from 'next/link';
import useSWR from 'swr';


import useSWRInfinite from 'swr/infinite'

import fetch from 'unfetch'

const fetcher = url => fetch(url).then(r => r.json())



const getKey = (fileIndex, previousPageData) => {
 // if (previousPageData && !previousPageData.length) return null // reached the end
  return `/api/event/${fileIndex}/`                    // SWR key
}



export default function Exhibitions() {

  let exhibitions = []
 
  let counter = 1;
  let size = 1;
  let data = {};
  let setSize = 21;

  let iterate = 1;
  while (iterate == 1){
    const { data, size, setSize } = useSWR(getKey(parseInt(counter)), fetcher)
    if (data !== undefined ){
      data["exid"] = counter;
      exhibitions.push(data);
     
  }
  counter = counter + 1;
  if (counter > 30){iterate = 2; }
}
  
 




  return (


    <div className="container">
    <div>
  

 
  
</div>
    

    


        <div><Link href="/">Back to home</Link></div>
      <Head>
        <title> Alternative New York Exhibitions</title>
        
      
      </Head>


      <main>
        <h1 className="title">Exhibitions</h1>

        <p className="description">
          List of alternative New York exhibitions
        </p>
        <ol>
       
        {
        
      

        exhibitions.map((exhibition) => (
        <li><Link key={exhibition.exid} href={'/exhibition/' + exhibition.exid }>{exhibition._label}</Link></li>
      ))}
     
    </ol>

        <div className="grid">
         
        </div>
      </main>

  
    </div>
  )
}

