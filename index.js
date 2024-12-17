'use strict';

{
    // nodelistを取得
    const tabMenus = document.querySelectorAll('.tab__menu-item');
    console.log(tabMenus);
    // tab一つごとにtabSwitch関数を適用
    tabMenus.forEach((tabMenu) => {
        tabMenu.addEventListener('click', tabSwitch);
    })

    function tabSwitch(e) {
        // クリックされた要素のデータ属性を取得
        const tabTargetData = e.currentTarget.dataset.tab;

        // クリックされた要素の親要素を取得
        const tabList = e.currentTarget.closest('.tab__menu');
        // ('.tab__menu-item')を検索してすべて取得
        const tabItems = tabList.querySelectorAll('.tab__menu-item');
        // 兄弟要素のtab__panel内で('.tab__panel-box')を検索して、すべて取得
        const tabPanelItems = tabList.
            nextElementSibling.querySelectorAll('.tab__panel-box');

        // クリックされたtabの同階層のmenuとpanelのクラスを削除
        tabItems.forEach((tabItem) => {
            tabItem.classList.remove('is-active');
        })
        tabPanelItems.forEach((tabPanelItem) => {
            tabPanelItem.classList.remove('is-show');
        // クリックしたmenuにis-activeクラスを追加
        e.currentTarget.classList.add('is-active');
        // data-panelの値が、タブと中身で等しければクラスを追加
        tabPanelItems.forEach((tabPanelItem) => {
            if (tabPanelItem.dataset.panel === tabTargetData) {
                tabPanelItem.classList.add('is-show')
            }
        })
        })
    }
}