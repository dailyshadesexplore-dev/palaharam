'use client'
import React, { useEffect, useState } from 'react';
import { useSearchParams } from 'next/navigation'
import Image from 'next/image';
import Form from 'next/form'

function Page() {
  const searchParams = useSearchParams()
  const cart = searchParams.get('cart');
  const cartData = cart ? JSON.parse(decodeURIComponent(cart)) : [];
  const paymentMode = [{
    name: 'Card',
    value: 'card'
  },
  {
    name: 'Cash',
    value: 'cash'
  }];
  const [checkoutResults, setCheckoutResults] = useState({
    'delivery_mode': '',
    'payment_mode': '',
    'First_Name': '',
    'Last_Name': '',
    'Street_Address': '',
    'Floor_Apt_Number': '',
    'State': '',
    'Zip': ''
  });
  const [selectedPayment, setSelectedPayment] = useState(checkoutResults.payment_mode || '');
  const [deliveryMode, setdeliveryMode] = useState(checkoutResults.delivery_mode || 'delivery');

  console.log(cartData)
  return (
    <div>
      <header className='border-b-4 border-gray-200 flex items-center justify-between w-full p-4'>
        <div>
          <button className='flex items-center gap-2'>
            <Image
              src={'/Images/back.png'}
              width={25}
              height={25}
              alt="back"
              className='drop-shadow-lg'
            />
            <p>Back to menu</p>
          </button>
        </div>
        <div className='flex items-center gap-0'>
          <Image
            src={'/Images/teaCuph.png'}
            width={40}
            height={40}
            alt='title'
          />
          <h1 className='font-bold text-lg'>PALAHARAM</h1>
        </div>
        <div></div>
      </header>
      <main className='absolute flex flex-col items-center w-full'>
        <div className='flex items-baseline p-2'>
          <div className=' flex flex-col items-center w-fit h-fit'>
            <p className='rounded-full bg-black text-white border-black border-4 w-fit px-2 h-fit'>1</p>
            <p>Checkout</p>
          </div>
          <div>
            ----------------------------------
          </div>
          <div className=' flex flex-col items-center'>
            <p className='rounded-full border-black border-2 w-fit px-2 h-fit'>2</p>
            <p>Payment</p>
          </div>
        </div>
        {/* PickUp or Delivery */}
        <div className='w-full flex items-center justify-between gap-8 p-6'>
          <div className='w-full'>
            <div className='w-full flex items-center justify-between'>
              <select value={deliveryMode} onChange={(e) => {
                setdeliveryMode(e.target.value);
                setCheckoutResults(prev => ({ ...prev, delivery_mode: e.target.value }));
              }} className="border border-black-2 rounded-lg p-2 w-1/4 bg-black text-white" name="delivery_mode" id="delivery_mode">
                <option value={'delivery'}>Delivery</option>
                <option value={'pickup'}>PickUp</option>
              </select>
              <div className="flex items-center gap-4 justify-evenly rounded-lg p-2 w-1/2 text-lg">
                {paymentMode.map((it, index) => (
                  <div key={index} className='flex gap-1 items-center'>
                    <input
                      type='radio'
                      id={`payment-${it.value}`}
                      name='payment_mode'
                      value={it.value}
                      checked={selectedPayment === it.value}
                      onChange={() => {
                        setSelectedPayment(it.value);
                        setCheckoutResults(prev => ({ ...prev, payment_mode: it.value }));
                      }}
                    />
                    <label htmlFor={`payment-${it.value}`}>{it.name}</label>
                  </div>
                ))}
              </div>

            </div>
            <div>
              {deliveryMode === "delivery" ? <Form action={'/checkOutFormAct'} className='flex flex-col w-full items-center gap-8 mt-4 font-sans'>
                {/* hidden inputs so payment_mode and delivery_mode are submitted with the form */}
                <input type="hidden" name="payment_mode" value={selectedPayment} />
                <input type="hidden" name="delivery_mode" value={deliveryMode} />
                <div className='w-full flex gap-4'>
                  <input name="First_Name" placeholder='First Name' value={checkoutResults.First_Name}
                    onChange={(e) => setCheckoutResults(prev => ({ ...prev, First_Name: e.target.value }))}
                    className='bg-white tracking-wide p-2 w-1/2 h-12 rounded-lg border-none  border-gray-300 border-2 placeholder:text-gray-400 placeholder:text-xl ' />
                  <input name="Last_Name" placeholder='Last Name' value={checkoutResults.Last_Name}
                    onChange={(e) => setCheckoutResults(prev => ({ ...prev, Last_Name: e.target.value }))}
                    className='bg-white p-2 w-1/2 h-12 rounded-lg border-none  border-gray-300 border-2 placeholder:text-gray-400 placeholder:text-xl ' />
                </div>
                <input name="Street_Address" placeholder='Street Address' value={checkoutResults.Street_Address}
                  onChange={(e) => setCheckoutResults(prev => ({ ...prev, Street_Address: e.target.value }))}
                  className='bg-white p-2 w-full h-12 rounded-lg border-none  border-gray-300 border-2 placeholder:text-gray-400 placeholder:text-xl ' />
                <div className='w-full flex gap-4'>
                  <input name="Floor_Apt_Number" placeholder='Floor or Apt Number' value={checkoutResults.Floor_Apt_Number}
                    onChange={(e) => setCheckoutResults(prev => ({ ...prev, Floor_Apt_Number: e.target.value }))}
                    className='bg-white p-2 w-1/2 h-12 rounded-lg border-none  border-gray-300 border-2 placeholder:text-gray-400 placeholder:text-xl ' />
                  <input name="State" placeholder='State' value={checkoutResults.State}
                    onChange={(e) => setCheckoutResults(prev => ({ ...prev, State: e.target.value }))}
                    className='bg-white p-2 w-1/2 h-12 rounded-lg border-none  border-gray-300 border-2 placeholder:text-gray-400 placeholder:text-xl ' />
                  <input name="Zip" placeholder='Zip' value={checkoutResults.Zip}
                    onChange={(e) => setCheckoutResults(prev => ({ ...prev, Zip: e.target.value }))}
                    className='bg-white p-2 w-1/2 h-12 rounded-lg border-none  border-gray-300 border-2 placeholder:text-gray-400 placeholder:text-xl ' />
                </div>
                <div className='w-full flex gap-4'>
                  <button className='w-full border-black border-4 rounded-lg h-16'>
                    Cancel
                  </button>
                  <button type="submit" className='w-full bg-black border-black border-4 rounded-lg h-16 text-white'>
                    Submit
                  </button>
                </div>
              </Form> :
                <div className='bg-white text-2xl p-4 font-bold rounded-xl text-slate-400 mt-4'>
                  <h1>Palaharam</h1><br />
                  <p>1-2-3, Ladoo Colony, Halwa Area</p><br />
                  <p>Hyderabad, Telengana</p><br />
                  <p>India</p>
                  <a className="flex items-center justify-start w-fit mt-8" href="https://maps.app.goo.gl/HNnQAKtN7JsJ8oaX8" target='blank'>
                    <Image
                      src={'/Images/map.png'}
                      width={20}
                      height={100}
                      alt='map'
                    />
                    <p className='text-lg text-blue-600 font-bold '><u>Open in the maps</u></p>
                  </a>
                </div>}
            </div>
          </div>
          <div className='w-full bg-slate-200 rounded-lg h-full drop-shadow-lg p-4'>
            <div className='flex flex-col'>
              {cartData && <div>
                {cartData.map((it, index) =>
                  <span className="flex items-center" key={index}><p>{it.item}</p> * <p>{it.count}</p></span>
                )}
              </div>}
              <p className='text-center'>Nothing in the cart</p>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}

export default Page