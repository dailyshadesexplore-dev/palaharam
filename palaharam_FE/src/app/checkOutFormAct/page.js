'use client'
import Image from 'next/image';
import { useEffect } from "react";
import AOS from 'aos';
import 'aos/dist/aos.css';
import { useRouter } from 'next/navigation';
function Page({message}) {
    const router = useRouter();

    useEffect(()=>{
  AOS.init();
  const interval = setInterval(() => {
          router.push('/');
  }, 5000);
  return()=> clearInterval(interval)
    },[])
  return (
    <div className=' opacity-100 flex flex-col justify-center items-center h-screen '>
      <div className='flex gap-2 items-center'>
      <p className='text-5xl'>{message?.message}</p>
      <Image
      src={'/Images/check-mark.png'}
      width={100}
      height={100}
      alt='check'
       data-aos="zoom-in-down"
      data-aos-duration="1000"
          data-aos-once="false"
    data-aos-easing="ease-in-out"
      />
      </div>
      <p className='text-3xl italic'>Order No: {message?.id}</p>
    </div>
  );
}

export default Page