<template>
  <div id="radioCard" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 xl:grid-cols-8 gap-4 mt-4">
    
    <div class="bg-white p-2 sm:p-4 md:p-6 rounded-lg shadow-lg text-center relative group">
      <img 
        src="/images/BBC_World_Service.png" 
        alt="BBC World Service logo" 
        @click="onPlayStream('https://lsn.lv/bbcradio.m3u8?station=bbc_world_service&bitrate=320000', 'BBC World Service', 'Live Radio')"
        class="mx-auto h-24 w-24 sm:h-28 sm:w-28 md:h-32 md:w-32 object-contain cursor-pointer transition-transform duration-200 hover:scale-110"
      >
    </div>

    <div class="bg-white p-2 sm:p-4 md:p-6 rounded-lg shadow-lg text-center relative group">
      <img 
        src="/images/BBC_Asian_Network.png" 
        alt="BBC Asian Network logo" 
        @click="onPlayStream('https://lsn.lv/bbcradio.m3u8?station=bbc_asian_network&bitrate=320000', 'BBC Asian Network', 'Live Radio')"
        class="mx-auto h-24 w-24 sm:h-28 sm:w-28 md:h-32 md:w-32 object-contain cursor-pointer transition-transform duration-200 hover:scale-110"
      >
    </div>

    <div class="bg-white p-2 sm:p-4 md:p-6 rounded-lg shadow-lg text-center relative group">
      <img 
        src="/images/BBC_Radio_London.png" 
        alt="BBC Radio London logo" 
        @click="onPlayStream('https://lsn.lv/bbcradio.m3u8?station=bbc_london&bitrate=320000', 'BBC Radio London', 'Live Radio')"
        class="mx-auto h-24 w-24 sm:h-28 sm:w-28 md:h-32 md:w-32 object-contain cursor-pointer transition-transform duration-200 hover:scale-110"
      >
    </div>


    <div class="bg-white p-2 sm:p-4 md:p-6 rounded-lg shadow-lg text-center relative group">
      <img 
        src="/images/LBC_News.png" 
        alt="LBC_News logo" 
        @click="onPlayStream('https://media-ice.musicradio.com/LBC1152', 'LBC_News', 'Live Radio')"
        class="mx-auto h-24 w-24 sm:h-28 sm:w-28 md:h-32 md:w-32 object-contain cursor-pointer transition-transform duration-200 hover:scale-110"
      >
    </div>

    <div class="bg-white p-2 sm:p-4 md:p-6 rounded-lg shadow-lg text-center relative group">
      <img 
        src="/images/LBC_London.png" 
        alt="LBC_London logo" 
        @click="onPlayStream('https://media-ssl.musicradio.com/LBCLondon', 'LBC_London', 'Live Radio')"
        class="mx-auto h-24 w-24 sm:h-28 sm:w-28 md:h-32 md:w-32 object-contain cursor-pointer transition-transform duration-200 hover:scale-110"
      >
    </div>

    <div class="bg-white p-2 sm:p-4 md:p-6 rounded-lg shadow-lg text-center relative group">
      <img 
        src="/images/Classical_FM.png" 
        alt="Classical_FM logo" 
        @click="onPlayStream('https://media-the.musicradio.com/ClassicFM', 'Classical FM', 'Live Radio')"
        class="mx-auto h-24 w-24 sm:h-28 sm:w-28 md:h-32 md:w-32 object-contain cursor-pointer transition-transform duration-200 hover:scale-110"
      >
    </div>
    
    <div class="bg-white p-2 sm:p-4 md:p-6 rounded-lg shadow-lg text-center relative group">
      <img 
        src="/images/Gold.jpg" 
        alt="Gold logo" 
        @click="onPlayStream('https://media-ssl.musicradio.com/Gold', 'Gold', 'Live Radio')"
        class="mx-auto h-24 w-24 sm:h-28 sm:w-28 md:h-32 md:w-32 object-contain cursor-pointer transition-transform duration-200 hover:scale-110"
      >
    </div>

    <div class="bg-white p-2 sm:p-4 md:p-6 rounded-lg shadow-lg text-center relative group">
      <img 
        src="/images/icrt.jpg" 
        alt="Icrt logo" 
        @click="onPlayStream('https://stream.rcs.revma.com/nkdfurztxp3vv', 'Icrt', 'Live Radio')"
        class="mx-auto h-24 w-24 sm:h-28 sm:w-28 md:h-32 md:w-32 object-contain cursor-pointer transition-transform duration-200 hover:scale-110"
      >
    </div>

    <div class="bg-white p-2 sm:p-4 md:p-6 rounded-lg shadow-lg text-center relative group">
      <img 
        src="/images/BBC_Radio_1.png" 
        alt="BBC_Radio_1 logo" 
        @click="onPlayStream('https://lsn.lv/bbcradio.m3u8?station=bbc_radio_one&bitrate=320000', 'BBC Radio 1', 'Live Radio')"
        class="mx-auto h-24 w-24 sm:h-28 sm:w-28 md:h-32 md:w-32 object-contain cursor-pointer transition-transform duration-200 hover:scale-110"
      >
    </div>

    <div class="bg-white p-2 sm:p-4 md:p-6 rounded-lg shadow-lg text-center relative group">
      <img 
        src="/images/BBC_Radio_2.png" 
        alt="BBC_Radio_2 logo" 
        @click="onPlayStream('https://lsn.lv/bbcradio.m3u8?station=bbc_radio_two&bitrate=320000', 'BBC Radio 2', 'Live Radio')"
        class="mx-auto h-24 w-24 sm:h-28 sm:w-28 md:h-32 md:w-32 object-contain cursor-pointer transition-transform duration-200 hover:scale-110"
      >
    </div>

    <div class="bg-white p-2 sm:p-4 md:p-6 rounded-lg shadow-lg text-center relative group">
      <img 
        src="/images/BBC_Radio_3.png" 
        alt="BBC_Radio_3 logo" 
        @click="onPlayStream('https://lsn.lv/bbcradio.m3u8?station=bbc_radio_three&bitrate=320000', 'BBC Radio 3', 'Live Radio')"
        class="mx-auto h-24 w-24 sm:h-28 sm:w-28 md:h-32 md:w-32 object-contain cursor-pointer transition-transform duration-200 hover:scale-110"
      >
    </div>

    <div class="bg-white p-2 sm:p-4 md:p-6 rounded-lg shadow-lg text-center relative group">
      <img 
        src="/images/BBC_Radio_4.png" 
        alt="BBC_Radio_4 logo" 
        @click="onPlayStream('https://lsn.lv/bbcradio.m3u8?station=bbc_radio_fourfm&bitrate=320000', 'BBC Radio 4', 'Live Radio')"
        class="mx-auto h-24 w-24 sm:h-28 sm:w-28 md:h-32 md:w-32 object-contain cursor-pointer transition-transform duration-200 hover:scale-110"
      >
    </div>

    <div class="bg-white p-2 sm:p-4 md:p-6 rounded-lg shadow-lg text-center relative group">
      <img 
        src="/images/BBC_Radio_5.png" 
        alt="BBC_Radio_5 logo" 
        @click="onPlayStream('https://lsn.lv/bbcradio.m3u8?station=bbc_radio_five_live&bitrate=320000', 'BBC Radio 5 Live', 'Live Radio')"
        class="mx-auto h-24 w-24 sm:h-28 sm:w-28 md:h-32 md:w-32 object-contain cursor-pointer transition-transform duration-200 hover:scale-110"
      >
    </div>

    <div class="bg-white p-2 sm:p-4 md:p-6 rounded-lg shadow-lg text-center relative group">
      <img 
        src="/images/BBC_Radio_6.png" 
        alt="BBC_Radio_6 logo" 
        @click="onPlayStream('https://lsn.lv/bbcradio.m3u8?station=bbc_6music&bitrate=320000', 'BBC Radio 6 Live', 'Live Radio')"
        class="mx-auto h-24 w-24 sm:h-28 sm:w-28 md:h-32 md:w-32 object-contain cursor-pointer transition-transform duration-200 hover:scale-110"
      >
    </div>

    <div class="bg-white p-2 sm:p-4 md:p-6 rounded-lg shadow-lg text-center relative group">
      <img 
        src="/images/Classical_Hits_1000.jpg" 
        alt="Classical_Hits_1000 logo" 
        @click="onPlayStream('https://radio2.vip-radios.fm:18042/stream-128kmp3-HitsClassical', 'Classical Hits', 'Live Radio')"
        class="mx-auto h-24 w-24 sm:h-28 sm:w-28 md:h-32 md:w-32 object-contain cursor-pointer transition-transform duration-200 hover:scale-110"
      >
    </div>

    <div class="bg-white p-2 sm:p-4 md:p-6 rounded-lg shadow-lg text-center relative group">
      <img 
        src="/images/Classical_Mozart.jpg" 
        alt="Classical_Mozart logo" 
        @click="onPlayStream('https://stream.klassikradio.de/mozart/mp3-192/mytune', 'Classical Mozart', 'Live Radio')"
        class="mx-auto h-24 w-24 sm:h-28 sm:w-28 md:h-32 md:w-32 object-contain cursor-pointer transition-transform duration-200 hover:scale-110"
      >
    </div>

    <div class="bg-white p-2 sm:p-4 md:p-6 rounded-lg shadow-lg text-center relative group">
      <img 
        src="/images/SKY_News.png" 
        alt="SKY_News logo" 
        @click="onPlayStream('https://video.news.sky.com/snr/news/snrnews.mp3', 'Sky News', 'Live Radio')"
        class="mx-auto h-24 w-24 sm:h-28 sm:w-28 md:h-32 md:w-32 object-contain cursor-pointer transition-transform duration-200 hover:scale-110"
      >
    </div>

    <div class="bg-white p-2 sm:p-4 md:p-6 rounded-lg shadow-lg text-center relative group">
      <img 
        src="/images/TIMES_Radio.png" 
        alt="TIMES_Radio logo" 
        @click="onPlayStream('https://timesradio.wireless.radio/stream?aw_0_1st.platform=website&aw_0_1st.playerid=wireless-website', 'Times Radio', 'Live Radio')"
        class="mx-auto h-24 w-24 sm:h-28 sm:w-28 md:h-32 md:w-32 object-contain cursor-pointer transition-transform duration-200 hover:scale-110"
      >
    </div>

    <div class="bg-white p-2 sm:p-4 md:p-6 rounded-lg shadow-lg text-center relative group">
      <img 
        src="/images/BBC_Radio_Wales.png" 
        alt="BBC_Radio_Wales logo" 
        @click="onPlayStream('https://lsn.lv/bbcradio.m3u8?station=bbc_radio_wales_fm&bitrate=320000', 'BBC Radio Wales', 'Live Radio')"
        class="mx-auto h-24 w-24 sm:h-28 sm:w-28 md:h-32 md:w-32 object-contain cursor-pointer transition-transform duration-200 hover:scale-110"
      >
    </div>

    <div class="bg-white p-2 sm:p-4 md:p-6 rounded-lg shadow-lg text-center relative group">
      <img 
        src="/images/BBC_Radio_Leeds.png" 
        alt="BBC_Radio_Leeds logo" 
        @click="onPlayStream('https://lsn.lv/bbcradio.m3u8?station=bbc_radio_leeds&bitrate=320000', 'BBC Radio Leeds', 'Live Radio')"
        class="mx-auto h-24 w-24 sm:h-28 sm:w-28 md:h-32 md:w-32 object-contain cursor-pointer transition-transform duration-200 hover:scale-110"
      >
    </div>

    <div class="bg-white p-2 sm:p-4 md:p-6 rounded-lg shadow-lg text-center relative group">
      <img 
        src="/images/TW_FM96.jpg" 
        alt="TW FM96 logo" 
        @click="onPlayStream('https://stream.rcs.revma.com/ndk05tyy2tzuv', 'TW FM96', 'Live Radio')"
        class="mx-auto h-24 w-24 sm:h-28 sm:w-28 md:h-32 md:w-32 object-contain cursor-pointer transition-transform duration-200 hover:scale-110"
      >
    </div>

    <div class="bg-white p-2 sm:p-4 md:p-6 rounded-lg shadow-lg text-center relative group">
      <img 
        src="/images/TW_FM103.jpg" 
        alt="TW FM103 logo" 
        @click="onPlayStream('https://stream.rcs.revma.com/aw9uqyxy2tzuv', 'TW FM103', 'Live Radio')"
        class="mx-auto h-24 w-24 sm:h-28 sm:w-28 md:h-32 md:w-32 object-contain cursor-pointer transition-transform duration-200 hover:scale-110"
      >
    </div>

    <div class="bg-white p-2 sm:p-4 md:p-6 rounded-lg shadow-lg text-center relative group">
      <img 
        src="/images/ASIAFM_927.jpg" 
        alt="ASIAFM 927 logo" 
        @click="onPlayStream('https://stream.rcs.revma.com/xpgtqc74hv8uv', 'ASIAFM 927', 'Live Radio')"
        class="mx-auto h-24 w-24 sm:h-28 sm:w-28 md:h-32 md:w-32 object-contain cursor-pointer transition-transform duration-200 hover:scale-110"
      >
    </div>

    <div class="bg-white p-2 sm:p-4 md:p-6 rounded-lg shadow-lg text-center relative group">
      <img 
        src="/images/UFO_Network.jpg" 
        alt="UFO Network logo" 
        @click="onPlayStream('https://n17a-eu.rcs.revma.com/em90w4aeewzuv?rj-tok=AAABmP7objYAlBv1a7_GA_pPZw&rj-ttl=5', 'UFO Network', 'Live Radio')"
        class="mx-auto h-24 w-24 sm:h-28 sm:w-28 md:h-32 md:w-32 object-contain cursor-pointer transition-transform duration-200 hover:scale-110"
      >
    </div>

    <div class="bg-white p-2 sm:p-4 md:p-6 rounded-lg shadow-lg text-center relative group">
      <img 
        src="/images/Hits_Radio.jpg" 
        alt="Hits Radio logo" 
        @click="onPlayStream('https://18853.live.streamtheworld.com/977_HITS_SC', 'Hits Radio', 'Live Radio')"
        class="mx-auto h-24 w-24 sm:h-28 sm:w-28 md:h-32 md:w-32 object-contain cursor-pointer transition-transform duration-200 hover:scale-110"
      >
      <div v-if="loadingStreamTitle === 'Hits Radio'" class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 text-white rounded-lg">
        <svg class="w-12 h-12 animate-spin" fill="currentColor" viewBox="0 0 20 20"><path d="M4 2a2 2 0 00-2 2v12a2 2 0 002 2h12a2 2 0 002-2V4a2 2 0 00-2-2H4z"/></svg>
      </div>
      <div v-else-if="isPlayingLiveStream && currentStreamInfo?.title === 'Hits Radio'" class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 text-white rounded-lg">
        <svg class="w-12 h-12" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832L12 10.202V12a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2A1 1 0 0012 8v1.798l-2.445-1.63z" clipRule="evenodd"/></svg>
      </div>
    </div>

    <div class="bg-white p-2 sm:p-4 md:p-6 rounded-lg shadow-lg text-center relative group">
      <img 
        src="/images/RTHK_Radio1.png" 
        alt="RTHK Radio1 logo" 
        @click="onPlayStream('https://rthkaudio1-lh.akamaihd.net/i/radio1_1@355864/index_56_a-p.m3u8', 'RTHK Radio1', 'Live Radio')"
        class="mx-auto h-24 w-24 sm:h-28 sm:w-28 md:h-32 md:w-32 object-contain cursor-pointer transition-transform duration-200 hover:scale-110"
      >
      <div v-if="loadingStreamTitle === 'RTHK Radio1'" class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 text-white rounded-lg">
        <svg class="w-12 h-12 animate-spin" fill="currentColor" viewBox="0 0 20 20"><path d="M4 2a2 2 0 00-2 2v12a2 2 0 002 2h12a2 2 0 002-2V4a2 2 0 00-2-2H4z"/></svg>
      </div>
      <div v-else-if="isPlayingLiveStream && currentStreamInfo?.title === 'RTHK Radio1'" class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 text-white rounded-lg">
        <svg class="w-12 h-12" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832L12 10.202V12a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2A1 1 0 0012 8v1.798l-2.445-1.63z" clipRule="evenodd"/></svg>
      </div>
    </div>


    <div class="bg-white p-2 sm:p-4 md:p-6 rounded-lg shadow-lg text-center relative group">
      <img 
        src="/images/RTHK_Radio2.svg" 
        alt="RTHK Radio2 logo" 
        @click="onPlayStream('	https://rthkaudio2-lh.akamaihd.net/i/radio2_1@355865/index_56_a-p.m3u8', 'RTHK Radio2', 'Live Radio')"
        class="mx-auto h-24 w-24 sm:h-28 sm:w-28 md:h-32 md:w-32 object-contain cursor-pointer transition-transform duration-200 hover:scale-110"
      >
      <div v-if="loadingStreamTitle === 'RTHK Radio2'" class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 text-white rounded-lg">
        <svg class="w-12 h-12 animate-spin" fill="currentColor" viewBox="0 0 20 20"><path d="M4 2a2 2 0 00-2 2v12a2 2 0 002 2h12a2 2 0 002-2V4a2 2 0 00-2-2H4z"/></svg>
      </div>
      <div v-else-if="isPlayingLiveStream && currentStreamInfo?.title === 'RTHK Radio2'" class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 text-white rounded-lg">
        <svg class="w-12 h-12" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832L12 10.202V12a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2A1 1 0 0012 8v1.798l-2.445-1.63z" clipRule="evenodd"/></svg>
      </div>
    </div>

    <div class="bg-white p-2 sm:p-4 md:p-6 rounded-lg shadow-lg text-center relative group">
      <img 
        src="/images/RTHK_Radio3.webp" 
        alt="RTHK Radio3 logo" 
        @click="onPlayStream('https://rthkaudio3-lh.akamaihd.net/i/radio3_1@355866/index_56_a-p.m3u8', 'RTHK Radio3', 'Live Radio')"
        class="mx-auto h-24 w-24 sm:h-28 sm:w-28 md:h-32 md:w-32 object-contain cursor-pointer transition-transform duration-200 hover:scale-110"
      >
      <div v-if="loadingStreamTitle === 'RTHK Radio3'" class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 text-white rounded-lg">
        <svg class="w-12 h-12 animate-spin" fill="currentColor" viewBox="0 0 20 20"><path d="M4 2a2 2 0 00-2 2v12a2 2 0 002 2h12a2 2 0 002-2V4a2 2 0 00-2-2H4z"/></svg>
      </div>
      <div v-else-if="isPlayingLiveStream && currentStreamInfo?.title === 'RTHK Radio3'" class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 text-white rounded-lg">
        <svg class="w-12 h-12" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832L12 10.202V12a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2A1 1 0 0012 8v1.798l-2.445-1.63z" clipRule="evenodd"/></svg>
      </div>
    </div>

    <div class="bg-white p-2 sm:p-4 md:p-6 rounded-lg shadow-lg text-center relative group">
      <img 
        src="/images/RTHK_Radio4.webp" 
        alt="RTHK Radio4 logo" 
        @click="onPlayStream('https://rthkradio4-live.akamaized.net/hls/live/2040080/radio4/master.m3u8', 'RTHK Radio4', 'Live Radio')"
        class="mx-auto h-24 w-24 sm:h-28 sm:w-28 md:h-32 md:w-32 object-contain cursor-pointer transition-transform duration-200 hover:scale-110"
      >
      <div v-if="loadingStreamTitle === 'RTHK Radio4'" class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 text-white rounded-lg">
        <svg class="w-12 h-12 animate-spin" fill="currentColor" viewBox="0 0 20 20"><path d="M4 2a2 2 0 00-2 2v12a2 2 0 002 2h12a2 2 0 002-2V4a2 2 0 00-2-2H4z"/></svg>
      </div>
      <div v-else-if="isPlayingLiveStream && currentStreamInfo?.title === 'RTHK Radio4'" class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 text-white rounded-lg">
        <svg class="w-12 h-12" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832L12 10.202V12a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2A1 1 0 0012 8v1.798l-2.445-1.63z" clipRule="evenodd"/></svg>
      </div>
    </div>

    <div class="bg-white p-2 sm:p-4 md:p-6 rounded-lg shadow-lg text-center relative group">
      <img 
        src="/images/RTHK_Radio5.webp" 
        alt="RTHK Radio5 logo" 
        @click="onPlayStream('https://rthkaudio5-lh.akamaihd.net/i/radio5_1@355868/index_56_a-p.m3u8', 'RTHK Radio5', 'Live Radio')"
        class="mx-auto h-24 w-24 sm:h-28 sm:w-28 md:h-32 md:w-32 object-contain cursor-pointer transition-transform duration-200 hover:scale-110"
      >
      <div v-if="loadingStreamTitle === 'RTHK Radio5'" class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 text-white rounded-lg">
        <svg class="w-12 h-12 animate-spin" fill="currentColor" viewBox="0 0 20 20"><path d="M4 2a2 2 0 00-2 2v12a2 2 0 002 2h12a2 2 0 002-2V4a2 2 0 00-2-2H4z"/></svg>
      </div>
      <div v-else-if="isPlayingLiveStream && currentStreamInfo?.title === 'RTHK Radio5'" class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 text-white rounded-lg">
        <svg class="w-12 h-12" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832L12 10.202V12a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2A1 1 0 0012 8v1.798l-2.445-1.63z" clipRule="evenodd"/></svg>
      </div>
    </div>


    <div class="bg-white p-2 sm:p-4 md:p-6 rounded-lg shadow-lg text-center relative group">
      <img 
        src="/images/RTHK_Putonghua_Radio.png" 
        alt="RTHK 普通話 logo" 
        @click="onPlayStream('https://stm.rthk.hk/radiopth', 'RTHK 普通話', 'Live Radio')"
        class="mx-auto h-24 w-24 sm:h-28 sm:w-28 md:h-32 md:w-32 object-contain cursor-pointer transition-transform duration-200 hover:scale-110"
      >
      <div v-if="loadingStreamTitle === 'RTHK 普通話'" class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 text-white rounded-lg">
        <svg class="w-12 h-12 animate-spin" fill="currentColor" viewBox="0 0 20 20"><path d="M4 2a2 2 0 00-2 2v12a2 2 0 002 2h12a2 2 0 002-2V4a2 2 0 00-2-2H4z"/></svg>
      </div>
      <div v-else-if="isPlayingLiveStream && currentStreamInfo?.title === 'RTHK 普通話'" class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 text-white rounded-lg">
        <svg class="w-12 h-12" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832L12 10.202V12a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2A1 1 0 0012 8v1.798l-2.445-1.63z" clipRule="evenodd"/></svg>
      </div>
    </div>

    <div class="bg-white p-2 sm:p-4 md:p-6 rounded-lg shadow-lg text-center relative group">
      <img 
        src="/images/BBC_Radio_Scotland.png" 
        alt="BBC Radio Scotland logo" 
        @click="onPlayStream('https://as-hls-ww.live.cf.md.bbci.co.uk/pool_43322914/live/ww/bbc_radio_scotland_fm/bbc_radio_scotland_fm.isml/bbc_radio_scotland_fm-audio%3d96000.norewind.m3u8', 'BBC Radio Scotland', 'Live Radio')"
        class="mx-auto h-24 w-24 sm:h-28 sm:w-28 md:h-32 md:w-32 object-contain cursor-pointer transition-transform duration-200 hover:scale-110"
      >
      <div v-if="loadingStreamTitle === 'BBC Radio Scotland'" class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 text-white rounded-lg">
        <svg class="w-12 h-12 animate-spin" fill="currentColor" viewBox="0 0 20 20"><path d="M4 2a2 2 0 00-2 2v12a2 2 0 002 2h12a2 2 0 002-2V4a2 2 0 00-2-2H4z"/></svg>
      </div>
      <div v-else-if="isPlayingLiveStream && currentStreamInfo?.title === 'BBC Radio Scotland'" class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 text-white rounded-lg">
        <svg class="w-12 h-12" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832L12 10.202V12a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2A1 1 0 0012 8v1.798l-2.445-1.63z" clipRule="evenodd"/></svg>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref } from 'vue';

// Get runtime config for the API base URL
const config = useRuntimeConfig();
const apiBase = config.public.apiBase;

const loading = ref(false);
const error = ref(null);
const channelName = useState('channelName', () => '');

const onPlayStream = async (url, title, artist) => {
  loading.value = true;
  error.value = null;

  channelName.value = title;

  console.log(`Requesting to play stream: ${title} from ${url}`);

  const token = localStorage.getItem('authToken');
  if (!token) {
    // Redirect to login or handle error
    window.location.href = '/login';
    return;
  }

  try {
    const response = await $fetch(`${apiBase}/pi_add_and_play_stream`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        stream_url: url,
        title: title,
        artist: artist
      })
    });

    if (response.status === 'success') {
      console.log('Stream added and is now playing.');
      // Optionally, you can emit an event to the parent to refresh its status
    } else {
      throw new Error(response.message || 'Failed to play stream');
    }
  } catch (err) {
    console.error('Error playing stream via MPD:', err);
    error.value = `Failed to play stream: ${err.message || 'Unknown error'}`;
    alert(`Error: ${error.value}`);
  } finally {
    loading.value = false;
  }
};
</script>
