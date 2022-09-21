import Head from 'next/head'
import Link from 'next/link';

export default function Artists() {
  return (
   
   
    <div className="container">
      <div><Link href="/">Back to home</Link> </div>
      <Head>
        <title>Alternative New York Exhibitions - Artists</title>
       
        
      </Head>

      <main>
        <h1 className="title">Artists</h1>
   
        <p className="description">
        A list of artists featured in alternative New York art exhibitions
        </p>

        <div className="grid">
          
        </div>
      </main>

      

     
    </div>
  
  
  
  
  )
}
