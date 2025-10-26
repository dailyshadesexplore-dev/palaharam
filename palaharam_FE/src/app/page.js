'use client'
import Image from "next/image";
import { useEffect,useState } from "react";
import AOS from 'aos';
import 'aos/dist/aos.css'; // <-- make sure this is here
import './mobile.css'
import Menu from './menu/page'

export default function Home() {
    const [showSplash, setShowSplash] = useState(true);

  useEffect(()=>{
AOS.init();
const interval = setInterval(() => {
  setShowSplash(false)
}, 5000);
return()=> clearInterval(interval)
  },[])
  return (
    <div className="overflow-hidden" >
    {showSplash?
      <div className="bg-black w-screen h-screen text-white overflow-hidden">
      <div className="fixed top-0 bottom-0 left-0 right-0 w-fit m-auto flex justify-center items-center ">
      <div
      className="h-full mt-[80%] -mr-24 splashScreenKettle"
        data-aos="zoom-in-down"
      data-aos-duration="1000"
          data-aos-once="false"
    data-aos-easing="ease-in-out"

      >
            <Image
      src={'/Images/TeaKettle.png'}
      width={200}
      height={200}
      alt="tea cup"
      className=""
      />
      </div>
      <div className="flex flex-col justify-center items-center">
      <div className="flex items-center justify-center">
        <p 
        data-aos="fade-up"
      data-aos-duration="1000"
    data-aos-easing="ease-in"
        className="text-3xl">|</p>
        <h1 
        data-aos="fade-left"
      data-aos-duration="1500"
          data-aos-delay="1000"
    data-aos-easing="ease-in"
        className="text-2xl">Palaharam</h1>
      </div>

      <Image
      src={'/Images/teaCup.png'}
      width={150}
      height={150}
      alt="tea cup"
      className=""
      />
      </div>
    </div> </div>:
  <Menu />
  }
  </div>
  );
}
