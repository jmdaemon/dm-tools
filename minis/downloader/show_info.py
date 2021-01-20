def printDownload(currentPage, pageIndex, saveAs):
    print(f'currentPage : {currentPage}')
    print(f'pageIndex   : {pageIndex}')
    print(f'saveAs      : {saveAs}')

def printMiniMetadata(mini_id, name, downloadLink):
    print(f"mini_id         : {mini_id}")
    print(f"name            : {name}")
    print(f"downloadLink    : {downloadLink}")
    print(f"")

def printQueues(pages, saved):
    # print(f"page: {pages.get()}\nsave: {saved.get()}", flush=True)
    print(f"page: {pages.get()}", flush=True)
    print(f"save: {saved.get()}", flush=True)

def printProductMetadata(mini_saved, mini_links):
    print(f"mini_saved  : {mini_saved.get()}", flush=True)
    print(f"mini_link   : {mini_links.get()}", flush=True)
