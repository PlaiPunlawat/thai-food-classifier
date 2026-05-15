import Link from "next/link";
import Image from "next/image";

export default function Navbar() {
  return (
    <>
      <div className="navbar bg-transparent">
        <div className="container mx-auto">
          <div className="flex-1">
            <Link href="/" className="text-xl text-white">
              <Image
                src="/images/tomyumkung.png"
                alt={"Tomyum Kung"}
                width={40}
                height={40}
                className="inline"
              />{" "}
              <span className="hidden sm:inline-block">WhatKind? ThaiFood!</span>
            </Link>
          </div>
          <div className="flex-none">
            <ul className="menu menu-horizontal p-0">
              <li>
                <Link href="/predict" className="font-bold">
                  Upload
                </Link>
              </li>
              <li>
                <Link href="/about" className="font-bold">
                  About us
                </Link>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </>
  );
}
