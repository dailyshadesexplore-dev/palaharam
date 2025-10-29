'use client'
import React, { useEffect, useState } from 'react';
import Image from "next/image";
import axios from 'axios';
import '../mobile.css'
import Link from 'next/link';
const Page = () => {
    const [menu, setMenu] = useState([])
    const [quantity, setQuatity] = useState({})
    const [cart, setCart] = useState([])
    useEffect(() => {
        axios.get('data/sample.json')
            .then((it) => {
                setMenu(it.data)
            })
            .catch((err) => {
                console.error("Error fetching menu:", err)
            })
    }, [])
    console.log(cart)
    return (
        <div className='overflow-hidden'>
            <header className='w-screen h-96 bg-gray-900 bg-[url(/Images/menuBanner.png)] bg-cover bg-blend-soft-light flex items-center justify-center'>
                <h1 className='text-[12vw] md:text-[10vw] lg:text-[15vw] font-bold text-center text-white'>PALAHARAM</h1>
            </header>
            <main className='flex flex-col items-center justify-center w-full mt-12'>

                {menu && menu.map((index, it) => (
                    <div key={it} className='border-b-1 border-gray-400 drop-shadow-lg p-8 flex items-center justify-between w-3/4 menuList'>
                        <div className='flex items-center gap-8 justify-between w-3/4 menuItems'>
                            {/* image */}
                            <Image
                                src={index.image}
                                width={200}
                                height={200}
                                alt="images"
                            />
                            {/* desciption */}
                            <div className='flex flex-col'>
                                <h1 className='font-bold text-xl'>{index.name}</h1>
                                <p className='text-sm'>{index.description}</p>
                            </div>
                        </div>

                        {/* cost and quantity*/}
                        <div className='flex flex-col items-end text-center w-1/4 justify-end menuCounter'>
                            <h1 className='font-bold text-center w-1/2 text-xl'>{index.values}</h1>
                            {/* quantity counter */}
                            <div className='flex items-center   justify-center w-1/2 '>
                                <button className='w-full rounded bg-green-600' onClick={() => {
                                    setQuatity((prev) => {
                                        const newQuantity = (prev[it] || 0) + 1;
                                        

                                        // update cart using the same newQuantity
                                        setCart((cartPrev) => {
                                            const existingItemIndex = cartPrev.findIndex((c) => c.item === index.name);
                                            if (existingItemIndex !== -1) {
                                                const updatedCart = [...cartPrev];
                                                updatedCart[existingItemIndex].count = newQuantity;
                                                updatedCart[existingItemIndex].value = index.values * newQuantity;

                                                return updatedCart;
                                            } else {
                                                return [...cartPrev, { item: index.name, count: newQuantity, value: index.values } ];
                                            }
                                        });

                                        return { ...prev, [it]: newQuantity };
                                    });
                                }}>+</button>
                                <p className='w-full text-center'>{quantity[it] || 0}</p>
                                <button
                                    className='w-full rounded bg-slate-300'
                                    onClick={() => {
                                        setQuatity((prev) => {
                                            const newQuantity = Math.max(0, (prev[it] || 0) - 1);
                                            
                                            // update cart using the same newQuantity
                                            setCart((cartPrev) => {
                                                const existingItemIndex = cartPrev.findIndex((c) => c.item === index.name);
                                                if (existingItemIndex !== -1) {
                                                    // If quantity becomes 0, remove the item from cart
                                                    if (newQuantity === 0) {
                                                        return cartPrev.filter((_, idx) => idx !== existingItemIndex);
                                                    } else {
                                                        // Otherwise, update the count
                                                        const updatedCart = [...cartPrev];
                                                        updatedCart[existingItemIndex].count = newQuantity;
                                                        return updatedCart;
                                                    }
                                                }
                                                // If item doesn't exist in cart and quantity is 0, don't add it
                                                return newQuantity > 0 ? [...cartPrev, { item: index.name, count: newQuantity }] : cartPrev;
                                            });

                                            return { ...prev, [it]: newQuantity };
                                        });
                                    }
                                    }
                                >-</button>
                            </div>
                        </div>
                    </div>))}

            </main>
            <footer className='p-4 fixed bottom-0 w-1/6 right-0 flex flex-col '>
                <div className='bg-slate-200 rounded-full w-fit h-fit p-2 drop-shadow-md'>
                    <b>{cart.length}</b>
                </div>
                <div className='p-2 py-4 bg-blue-500 rounded-full w-full h-fit text-center drop-shadow-md hover:outline-white hover:outline-2 hover:drop-shadow-lg cursor-pointer'>
                    <Link
                        href={{
                            pathname: '/checkOut',
                            query: { 
                                cart: encodeURIComponent(JSON.stringify(cart.filter(item => item.count > 0)))
                            }
                        }}
                        className='text-xl font-bold text-white w-full'>Checkout</Link>
                </div>
            </footer>
        </div>
    );
}

export default Page;
