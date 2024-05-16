import {
  Button,
  Card,
  Divider,
  TextInput,
} from "@tremor/react";
import { RiSearchLine } from '@remixicon/react';
import React from "react";
import axios from 'axios'
import { URL } from '../socket';
import LoadingDots from "../components/LoadingDots";

function Home() {
  const [product, setProduct] = React.useState([]);
  const [message, setMessage] = React.useState(null);
  const [search, setSearch] = React.useState(undefined);
  const [loading, setLoading] = React.useState(false);
  const [sse, setSse] = React.useState(null)

  const closeSse = () => {
    if (sse) {
      sse.close()
    }
    setMessage(null)
  }

  const listenSse = () => {
    const mysse = new EventSource(`${URL}/stream`)
    function handleStream(e) {
      setMessage(e.data)
    }
    mysse.onmessage = e => {handleStream(e)}
    setSse(mysse)
  }

  const handleClickSearch = async () => {
    listenSse()
    setLoading(true)
    setProduct([])
    // socket.emit('message', 'check status')
    await axios.get(`${URL}/api/product?name=${search}`)
    .then((res) => {
      setProduct(res.data.data)
    }).catch((err) => {
      console.log(err);
    })
    closeSse()
    setLoading(false)
  }

  return (
    <div className="h-full w-full bg-gray-50 px-3 py-5 xl:px-16 xl:py-12">
      <header className="ie-na-header flex w-full justify-between">
        <h3 className="text-xl font-semibold text-gray-900">So sánh giá</h3>
      </header>
      <div className="flex w-1/2 gap-2" >
        <TextInput 
          icon={RiSearchLine} 
          placeholder="Nhập tên sản phẩm..." 
          value={search} 
          onChange={(e) => {
            setSearch(e.target.value)
          }} 
          />
        <Button variant="secondary" disabled={loading} onClick={handleClickSearch}>Search</Button>
      </div>
      {loading && <LoadingDots message={message} />}
      {/* <LoadingDots message={message} /> */}
      <div className="grid ie-na-content mt-5 gap-10 sm:grid-cols-5">
        {product.map((item) => (
          <a href={item?.url}>
            <Card key={item?.id} className="space-y-4">
              <div className="aspect-square rounded-xl bg-gray-100 relative">
                <img
                  src={item?.image}
                  alt={item?.name}
                  className="aspect-square object-cover rounded-md w-full h-full"
                />
              </div>
              <p className="font-semibold text-md">{item?.name}</p>
              {/* <p className="truncate text-sm text-gray-500">{item.website}</p> */}
              <Divider>{item?.website}</Divider>
              <div className="flex items-center justify-between text-red-500">
                {item?.price}
              </div>
            </Card>
          </a>
        ))}
      </div>
    </div>
  );
}

export default Home;
