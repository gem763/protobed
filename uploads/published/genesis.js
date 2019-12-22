// 조상클래스
class Base {
  constructor() {
    this.copyright = 'flowrence 2019';
    this.author = undefined;
    this.created_at = undefined;
    this.nlike = 0;
    this.nshare = 0;
  }
}


// DataSourcer 조상클래스
export class BaseDataSourcer extends Base {
  async get() {}
}


// Visualizer 조상클래스
export class BaseVisualizer extends Base {
  constructor(dataSourcer) {
    super();
    this.dataSourcer = dataSourcer;
  }
  async show() {}
}


// miniapp 조상클래스
export class BaseMiniapp extends Base {
  constructor(DataSourcer, Visualizer) {
    super();
    this.dataSourcer = new DataSourcer()
    this.visualizer = new Visualizer(this.dataSourcer)
  }

  run(canvas, params) {
    return this.visualizer.show(canvas, params);
  }
}
