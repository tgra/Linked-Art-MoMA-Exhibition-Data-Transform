import { useRouter } from 'next/router';
import Link from 'next/link';
import Head from 'next/head';
import type { Event } from '../../interfaces'
import useSwr from 'swr'
import { resolve } from 'path';

const fetcher = (url: string) => fetch(url).then((res) => res.json())


const Exhibition = () => {
  const router = useRouter();
  const id = router.query;
  const { data, error } = useSwr<Event[]>('/api/event/' + id.id, fetcher)

  if (error) return <div>Failed to load exhibitions</div>
  if (!data) return <div>Loading...</div>
  
  console.log(data)
  // get file contents using id and api 

  return (
    <div className="container">
    <div></div>
        <div><Link href="/">Back to home</Link> / <Link href="/exhibition">Exhibitions</Link></div>
      <Head>
        <title> Alternative New York Exhibition</title>
        
      
      </Head>


      <div>
        <h2>Title</h2>
        <h3>{data._label}</h3>
        <h2>Date</h2>
        <p>Start: {data.timespan.begin_of_the_begin}   End: {data.timespan.end_of_the_end}</p>
        <h2>Location</h2>
        <p>{data.took_place_at[0]._label}</p>
        <h2>Agents associated with this exhibition</h2>
        {
        data.part[0].involved.map((set) => (
          
          <span>
            
          <h3>{set._label}</h3>
          <ol>
         
           { set.about.map((agent) => (
              <li key={agent.id}>{agent._label}</li>
            ))
           }
          </ol> 
          </span>    
        ))
        }
        
       
     
        </div>
        </div>


  )
}

export default Exhibition

