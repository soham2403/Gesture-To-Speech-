import React from "react";
import { Link } from "react-router-dom";

const Body = () => {
  return (
    <section class="bg-gray-800 text-white">
      <div class="mx-auto max-w-screen-xl px-4 py-32 lg:flex lg:h-screen lg:items-center">
        <div class="mx-auto max-w-3xl text-center">
          <h1 class="bg-gradient-to-r from-green-300 via-teal-500 to-blue-600 bg-clip-text text-3xl font-extrabold text-transparent sm:text-5xl">
            Welcome to Gesture to
            <span class="sm:block">Speech Translator </span>
          </h1>

          <p class="mx-auto mt-4 max-w-xl sm:text-xl/relaxed">
            Empowering communication through gestures
          </p>

          <div class="mt-8 flex flex-wrap justify-center gap-4">
            <Link
              class="block w-full rounded border border-teal-600 bg-teal-600 px-12 py-3 text-sm font-medium text-white hover:bg-transparent hover:text-white focus:outline-none focus:ring active:text-opacity-75 sm:w-auto"
              to="/optionPage"
            >
                Try Now
            </Link>

            <a
              class="block w-full rounded border border-teal-600 px-12 py-3 text-sm font-medium text-white hover:bg-teal-600 focus:outline-none focus:ring active:bg-teal-500 sm:w-auto"
              href="#"
            >
              Learn More
            </a>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Body;
