from pathlib import Path
import re
p=Path('/mnt/data/v47/showcase.js')
s=p.read_text()
start=s.index('async function fetchMostUnfetchedImage()')
end=s.index('$("#fetchMissingBtn")', start)
new=r'''async function inspectTweetPage(tweetId){
  const fn=async target=>{
    const sleep=ms=>new Promise(r=>setTimeout(r,ms));
    const topTweets=()=>[...document.querySelectorAll('article[data-testid="tweet"],article[role="article"]')].filter(a=>!a.parentElement?.closest('article[data-testid="tweet"],article[role="article"]'));
    const pick=(img,a)=>{
      const out=[];
      const add=v=>{v=String(v||'').trim();if(v&&!out.includes(v))out.push(v);};
      add(img?.currentSrc);add(img?.src);
      for(const attr of ['data-src','data-original','data-lazy-src','data-url'])add(img?.getAttribute?.(attr));
      for(const attr of ['srcset','data-srcset']){const raw=img?.getAttribute?.(attr)||'';for(const part of raw.split(',').map(v=>v.trim())){const u=part.split(/\s+/)[0];if(u)add(u);}}
      if(a){for(const link of a.querySelectorAll('a[href]')){const h=link.href||'';if(/pbs\.twimg\.com\/media\//i.test(h))add(h);for(const img2 of link.querySelectorAll('img')){add(img2.currentSrc);add(img2.src);}}}
      return out;
    };
    const extract=()=>{
      const articles=topTweets();
      const targetArticle=articles.find(article=>[...article.querySelectorAll('a[href*="/status/"]')].some(a=>String(a.href||'').match(new RegExp('/status/'+target+'(?:[/?#]|$)'))))||articles[0];
      if(!targetArticle)return null;
      const images=[];
      const add=v=>{if(v&&!images.includes(v))images.push(v)};
      for(const img of targetArticle.querySelectorAll('[data-testid="tweetPhoto"] img'))for(const v of pick(img,targetArticle))add(v);
      for(const img of targetArticle.querySelectorAll('img'))for(const v of pick(img,targetArticle))if(/pbs\.twimg\.com\/media\//i.test(v)||img.closest('[data-testid="tweetPhoto"]'))add(v);
      return {images,hasVideo:!!targetArticle.querySelector('[data-testid="videoPlayer"],video')};
    };
    for(let i=0;i<20;i++){
      const result=extract();
      if(result?.images?.length)return result;
      await sleep(500);
    }
    return extract()||{images:[],hasVideo:false};
  };
  const result=await chrome.scripting.executeScript({target:{tabId:inspectTweetPage.tabId},func:fn,args:[String(tweetId)]});
  return result?.[0]?.result||null;
}
async function waitForTabComplete(tabId,timeout=20000){
  try{const current=await chrome.tabs.get(tabId);if(current.status==='complete')return true;}catch{return false;}
  return new Promise(resolve=>{let done=false;const finish=value=>{if(done)return;done=true;clearTimeout(timer);chrome.tabs.onUpdated.removeListener(listener);resolve(value)};const listener=(id,changeInfo)=>{if(id===tabId&&changeInfo.status==='complete')finish(true)};const timer=setTimeout(()=>finish(false),timeout);chrome.tabs.onUpdated.addListener(listener)});
}
async function fetchMostUnfetchedImage(){
  if(state.imageFetchRunning)return;
  let candidates=imageCandidates();
  if(!candidates.length){updateFetchStatus('No unfetched-image candidates remain.');return;}
  const btn=$("#fetchMissingBtn");
  state.imageFetchRunning=true;btn.disabled=true;btn.textContent='Checking images…';
  let tab=null;
  try{
    const previous=await chrome.tabs.query({active:true,currentWindow:true});
    const previousTabId=previous[0]?.id||null;
    tab=await chrome.tabs.create({url:'about:blank',active:true});
    let foundImage=null;
    for(let i=0;i<candidates.length;i++){
      const item=candidates[i];
      updateFetchStatus(`Checking ${i+1.toLocaleString()} / ${candidates.length.toLocaleString()} · @${item.handle||'user'}…`);
      await chrome.tabs.update(tab.id,{url:item.tweetUrl,active:true});
      const loaded=await waitForTabComplete(tab.id,20000);
      let result=null;
      if(loaded){
        try{inspectTweetPage.tabId=tab.id;result=await inspectTweetPage(item.tweetId);}catch(error){result={images:[],error:String(error)}}
      }
      const checkedAt=new Date().toISOString();
      const updated={...item,imageFetchAttempts:Number(item.imageFetchAttempts||0)+1,imageLastCheckedAt:checkedAt};
      if(result?.images?.length)updated.images=[...new Set([...(updated.images||[]),...result.images])];
      if(result?.hasVideo)updated.hasVideo=true;
      const data=await chrome.storage.local.get('bookmarks');
      const archive=Array.isArray(data.bookmarks)?data.bookmarks:[];
      const merged=archive.map(saved=>String(saved?.tweetId)===String(updated.tweetId)?{...saved,...updated,collections:[...new Set([...(saved.collections||[]),...(updated.collections||[])])]}:saved);
      if(!merged.some(saved=>String(saved?.tweetId)===String(updated.tweetId)))merged.push(updated);
      await chrome.storage.local.set({bookmarks:merged,lastSavedAt:checkedAt});
      state.bookmarks=merged.map(saved=>({...saved,collections:collections(saved)}));buildIndex();render(true);
      candidates=imageCandidates();
      if(updated.images?.length){foundImage=updated;updateFetchStatus(`Image found for @${updated.handle||'user'}. ${candidates.length.toLocaleString()} posts remain without images.`);break;}
      updateFetchStatus(`No image found for @${updated.handle||'user'} · moving to the next post…`);
    }
    if(!foundImage)updateFetchStatus(`Finished checking ${candidates.length.toLocaleString()} unfetched-image candidates. No image was found.`);
  }catch(error){updateFetchStatus(`Image check failed: ${error.message||error}`);}finally{
    if(tab?.id)await chrome.tabs.remove(tab.id).catch(()=>{});
    const previousTabs=await chrome.tabs.query({active:true,currentWindow:true}).catch(()=>[]);
    if(previousTabs[0]?.id===tab?.id){}
    state.imageFetchRunning=false;btn.disabled=false;btn.textContent='Press to fetch most unfetched image';
  }
}
'''
# Remove weird previous tab unused logic by design; rewrite cleanly below.
s=s[:start]+new+s[end:]
p.write_text(s)
