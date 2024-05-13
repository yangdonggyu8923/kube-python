import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "@/app/style/globals.css";
import React from "react";
const inter = Inter({ subsets: ["latin"] });
export const metadata: Metadata = {
  title: "Create Next App",
  description: "Generated by create next app",
};
export default function RootLayout({
  children,modal
}: Readonly<{
  children: React.ReactNode,
  modal:React.ReactNode
}>) {
  return (
    <html lang="en" className="bg-blue-100 ">
      <body className="h-screen w-screen">
        {children}
        {modal}
        </body>
    </html>
  );
}